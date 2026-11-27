"""DocWeave: deterministic invoice extraction, region evidence and immutable artifacts."""
from pathlib import Path
from contextlib import contextmanager
from hashlib import sha256
import argparse,html,json,os,re,uuid
import pymupdf
from documents import inspect_pdf,line_table,evidence_for,validate_evidence
from contracts import Invoice,cents

RECIPE={'pipeline':'docweave-v1','native_pdf_only':True,'render_dpi':144,'table_strategy':'lines_strict','layout_model':False,'schema':'invoice-v1'}
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(value):return sha256(value).hexdigest()
def atomic_json(path,value):
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(canonical(value));os.replace(temp,path)
@contextmanager
def writer_lock(root):
    root.mkdir(parents=True,exist_ok=True);lock=root/'writer.lock'
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    try:os.write(fd,str(os.getpid()).encode());os.close(fd);fd=None;yield
    finally:
        if fd is not None:os.close(fd)
        lock.unlink(missing_ok=True)

def extract(source,document):
    if not document['pages'][0]['native_text']:raise ValueError('Scanned page needs explicit OCR and review; no guessed extraction')
    text=document['pages'][0]['text'];fields={};evidence={}
    patterns={'invoice_no':r'Invoice:\s*(DW-\d{4}-\d{3})','invoice_date':r'Date:\s*(\d{4}-\d{2}-\d{2})','currency':r'Currency:\s*(USD)',
              'subtotal_cents':r'Subtotal:\s*([0-9]+\.[0-9]{2})','tax_cents':r'Tax:\s*([0-9]+\.[0-9]{2})','total_cents':r'(?m)^Total:\s*([0-9]+\.[0-9]{2})'}
    for key,pattern in patterns.items():
        matches=list(re.finditer(pattern,text))
        if len(matches)!=1:raise ValueError('Missing or ambiguous field: '+key)
        raw=matches[0].group(1);fields[key]=cents(raw) if key.endswith('_cents') else raw
        evidence[key]=evidence_for(source,0,matches[0].group(0).strip());validate_evidence(document,evidence[key])
    invoice=Invoice.model_validate({**fields,'document_sha256':document['sha256'],'evidence':evidence})
    tables=line_table(source)
    if len(tables)!=1 or tables[0]['cells'][0]!=['Item','Qty','Unit','Amount']:raise ValueError('Unsupported invoice table')
    rows=tables[0]['cells'][1:];total=0
    for product,quantity,unit,amount in rows:
        if not quantity.isdecimal() or int(quantity)<1 or int(quantity)*cents(unit)!=cents(amount):raise ValueError('Line-item reconciliation failed')
        total+=cents(amount)
    if total!=invoice.subtotal_cents:raise ValueError('Table subtotal mismatch')
    return invoice.model_dump(),tables

def verify_version(root,manifest):
    if not re.fullmatch(r'[a-f0-9]{24}',manifest.get('version','')):raise ValueError('Invalid version')
    folder=(root/'versions'/manifest['version']).resolve()
    if not folder.is_relative_to((root/'versions').resolve()):raise ValueError('Path escaped workspace')
    required={'source.pdf','invoice.json','pages.json','tables.json','review.html','page-0.png'}
    if set(manifest.get('files',{}))!=required:raise ValueError('Incomplete artifact set')
    for name,expected in manifest['files'].items():
        target=(folder/name).resolve()
        if not target.is_relative_to(folder) or digest(target.read_bytes())!=expected:raise ValueError('Artifact integrity check failed')
    invoice=Invoice.model_validate_json((folder/'invoice.json').read_bytes())
    document=inspect_pdf(folder/'source.pdf')
    if document['sha256']!=invoice.document_sha256 or document['sha256']!=manifest['document_sha256']:raise ValueError('Source identity mismatch')
    for ev in invoice.evidence.values():validate_evidence(document,ev.model_dump())
    return manifest

def process(source,workspace,fault=None):
    source=Path(source);root=Path(workspace).resolve();document=inspect_pdf(source)
    page=document['pages'][0]
    if page['width']*page['height']*(RECIPE['render_dpi']/72)**2>8_000_000:raise ValueError('Rendered page exceeds pixel budget')
    version=digest(canonical({'document':document['sha256'],'recipe':RECIPE}))[:24]
    with writer_lock(root):
        folder=root/'versions'/version;folder.mkdir(parents=True,exist_ok=True);manifest_path=folder/'manifest.json'
        if manifest_path.exists():
            manifest=json.loads(manifest_path.read_bytes());verify_version(root,manifest)
            if manifest['document_sha256']!=document['sha256'] or manifest['recipe']!=RECIPE:raise ValueError('Cached recipe mismatch')
        else:
            invoice,tables=extract(source,document)
            (folder/'source.pdf').write_bytes(source.read_bytes());(folder/'invoice.json').write_bytes(canonical(invoice));(folder/'pages.json').write_bytes(canonical(document));(folder/'tables.json').write_bytes(canonical(tables))
            with pymupdf.open(source) as doc:
                pix=doc[0].get_pixmap(dpi=RECIPE['render_dpi'],alpha=False);pix.save(folder/'page-0.png')
            highlights=''.join(f'<rect x="{e["bbox"][0]}" y="{e["bbox"][1]}" width="{e["bbox"][2]-e["bbox"][0]}" height="{e["bbox"][3]-e["bbox"][1]}" fill="none" stroke="#9b1c31"><title>{html.escape(k)}</title></rect>' for k,e in invoice['evidence'].items())
            review=f'<!doctype html><html lang="en"><meta charset="utf-8"><title>DocWeave evidence review</title><style>body{{font:18px system-ui;background:#101713;color:#e5eee8;margin:30px}}svg{{max-width:700px;width:100%;background:white}}pre{{white-space:pre-wrap}}</style><h1>Synthetic invoice: evidence review</h1><p>Rule-based extraction; no VLM inference. Red outlines identify cited regions on page 1.</p><svg viewBox="0 0 612 792" role="img" aria-label="Invoice with extracted field regions"><image href="page-0.png" width="612" height="792"/>{highlights}</svg><pre>{html.escape(json.dumps(invoice,ensure_ascii=False,indent=2))}</pre><a href="source.pdf">Immutable source PDF</a></html>'
            (folder/'review.html').write_text(review,encoding='utf-8')
            names=['source.pdf','invoice.json','pages.json','tables.json','review.html','page-0.png']
            manifest={'version':version,'document_sha256':document['sha256'],'recipe':RECIPE,'files':{n:digest((folder/n).read_bytes()) for n in names}}
            atomic_json(manifest_path,manifest);verify_version(root,manifest)
        if fault=='after_artifacts':raise RuntimeError('Injected failure before current pointer')
        atomic_json(root/'current.json',manifest)
        return manifest

def read_current(workspace):
    root=Path(workspace).resolve();return verify_version(root,json.loads((root/'current.json').read_bytes()))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--workspace',type=Path,required=True);p.add_argument('--fault',choices=['after_artifacts']);a=p.parse_args();print(json.dumps(process(a.input,a.workspace,a.fault),ensure_ascii=False,indent=2))

"""Bounded parsing, native text, drawing-line tables and safe synthetic redaction."""
from pathlib import Path
from hashlib import sha256
import re
import pymupdf
from pypdf import PdfReader
from geometry import box

def inspect_pdf(path,max_pages=20,max_bytes=5_000_000):
    path=Path(path)
    with path.open('rb') as stream:raw=stream.read(max_bytes+1)
    if len(raw)>max_bytes or not raw.startswith(b'%PDF-'):raise ValueError('Not a bounded PDF input')
    with pymupdf.open(stream=raw,filetype='pdf') as doc:
        if doc.needs_pass:raise ValueError('Encrypted input requires a separate authorization workflow')
        if not 0<len(doc)<=max_pages:raise ValueError('Page budget exceeded')
        pages=[]
        for i,page in enumerate(doc):
            words=[{'bbox':list(w[:4]),'text':w[4],'block':w[5],'line':w[6]} for w in page.get_text('words',sort=False)]
            pages.append({'page_index':i,'width':page.cropbox.width,'height':page.cropbox.height,'rotation':page.rotation,'words':words,'text':page.get_text(sort=False),'native_text':bool(words)})
    return {'sha256':sha256(raw).hexdigest(),'pages':pages}

def compare_text(path):
    return [page.extract_text() or '' for page in PdfReader(path).pages]

def line_table(path,page_index=0):
    with pymupdf.open(path) as doc:
        # Explicitly disable model layout: the core lab is deterministic and offline.
        finder=doc[page_index].find_tables(strategy='lines_strict',use_layout=False)
        return [{'bbox':list(t.bbox),'cells':t.extract()} for t in finder.tables]

def reading_order(words,split_x=None):
    if split_x is None:return sorted(words,key=lambda w:(round(w['bbox'][1]/8),w['bbox'][0]))
    return sorted(words,key=lambda w:(w['bbox'][0]>=split_x,round(w['bbox'][1]/8),w['bbox'][0]))

def redact_demo(source,target,needle='demo@example.test'):
    if Path(source).resolve()==Path(target).resolve():raise ValueError('Preserve the source')
    with pymupdf.open(source) as doc:
        for page in doc:
            for rect in page.search_for(needle):page.add_redact_annot(rect,fill=(0,0,0))
            page.apply_redactions()
        doc.save(target,garbage=4,deflate=True)
    with pymupdf.open(target) as checked:
        if any(needle in p.get_text() for p in checked):raise ValueError('Text redaction verification failed')
    return str(target)

def evidence_for(path,page_index,text):
    with pymupdf.open(path) as doc:
        page=doc[page_index];matches=page.search_for(text)
        if len(matches)!=1:raise ValueError('Evidence must resolve to exactly one region')
        return {'page_index':page_index,'bbox':list(matches[0]),'quote':text}

def validate_evidence(document,evidence):
    p=evidence['page_index']
    if type(p) is not int or not 0<=p<len(document['pages']):raise ValueError('Unknown source page')
    page=document['pages'][p];rect=box(evidence['bbox'],page['width'],page['height'])
    words=[w for w in page['words'] if rect[0]-1<=w['bbox'][0] and rect[1]-1<=w['bbox'][1] and w['bbox'][2]<=rect[2]+1 and w['bbox'][3]<=rect[3]+1]
    text=' '.join(w['text'] for w in reading_order(words))
    squash=lambda s:re.sub(r'\s+','',s)
    if not evidence['quote'] or squash(evidence['quote']) not in squash(text):raise ValueError('Quote not present inside cited region')
    return True

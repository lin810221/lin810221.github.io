"""32 runnable labs. No external API calls; lab 07 runs bundled OCR weights."""
from contextlib import contextmanager
from pathlib import Path
from functools import lru_cache
import argparse,importlib.metadata,json,shutil,uuid
from fixtures import ROOT
from documents import inspect_pdf,compare_text,line_table,reading_order,redact_demo,evidence_for,validate_evidence
from geometry import normalize,pixels,rotate_clockwise,tiles,restore_crop,iou
from metrics import cer,anls,prf,maxsim,contrastive_loss,risk_coverage
from contracts import decide,Invoice
from providers import request_spec
from retrieval import chunks,lexical_search,fuse,answer_total
from media import audio_info,aligned_segments,segment_at,gif_frames
from pipeline import process,read_current,extract
LABS={
'01':'Modality routing and native-text inspection','02':'Installed version and environment audit',
'03':'Point, pixel and normalized coordinates','04':'Tiling, rotation and crop inverse',
'05':'Compare two actual PDF text extractors','06':'Detect a raster-only PDF without guessing text',
'07':'Real PP-OCRv6 CPU recognition with bundled weights','08':'Character edit distance and ANLS boundary',
'09':'Explicit two-column reading order','10':'Page/block/line document representation',
'11':'Real ruled-table extraction and reconciliation','12':'Actual AcroForm field versus printed text',
'13':'Strict Pydantic invoice and region evidence','14':'Unknown, review and accepted extraction decisions',
'15':'Symmetric image/text contrastive objective algebra','16':'Late interaction MaxSim algebra, no semantic model',
'17':'OpenAI Responses PDF request dry run','18':'Gemini Interactions and Claude Messages dry run',
'19':'Retrieved total with document/page provenance','20':'Reject a quote attached to an unrelated region',
'21':'Tenant filtering before document retrieval','22':'Reciprocal rank fusion of independent result lists',
'23':'Extraction precision, recall and F1','24':'Confidence threshold, risk and coverage',
'25':'Bounded PDF input rejection','26':'Real PDF redaction and text verification',
'27':'Actual WAV samples and authored transcript intervals','28':'Real animated GIF frame timestamps',
'29':'DocWeave immutable evidence artifacts','30':'Failure before pointer and deterministic recovery',
'31':'Artifact corruption detection','32':'Whole-project rerun and provenance acceptance'}

@contextmanager
def scratch():
    base=ROOT/'.runtime';base.mkdir(exist_ok=True);path=base/uuid.uuid4().hex;path.mkdir()
    try:yield path
    finally:shutil.rmtree(path)
@lru_cache(maxsize=1)
def ocr_fixture():
    from ocr_local import recognize
    return recognize(ROOT/'data/scan.png')
def run_lab(key):
    source=ROOT/'data/invoice.pdf';document=inspect_pdf(source)
    with scratch() as work:
        if key=='01':return [{'page':p['page_index'],'native':p['native_text']} for p in document['pages']]
        if key=='02':return {n:importlib.metadata.version(n) for n in ['pymupdf','pypdf','pillow','pydantic','rapidocr','onnxruntime']}
        if key=='03':return {'normalized':normalize([72,72,144,144],612,792),'pixels_144dpi':pixels([72,72,144,144],144),'overlap_iou':iou([0,0,2,2],[1,1,3,3])}
        if key=='04':return {'tiles':len(tiles(1200,800)),'rotated':rotate_clockwise([10,20,50,80],612,792),'restored':restore_crop([20,30,80,90],[100,200],2)}
        if key=='05':return {'engines':2,'pages':len(compare_text(source)),'both_find_total':all('47.25' in text for text in [document['pages'][0]['text'],compare_text(source)[0]])}
        if key=='06':return {'scan_has_native_text':inspect_pdf(ROOT/'data/scan.pdf')['pages'][0]['native_text'],'policy':'OCR explicitly; never invent empty-page fields'}
        if key=='07':
            r=ocr_fixture();return {'engine':r['engine'],'regions':len(r['texts']),'total_seen':any('47.25' in t for t in r['texts']),'model_sha256':r['models']}
        if key=='08':return {'cer':cer('4725','472S'),'anls_at_half':anls('AB','AC'),'empty_reference':cer('','x')}
        if key=='09':return [w['text'] for w in reading_order(document['pages'][1]['words'],306)]
        if key=='10':return [{'page':p['page_index'],'blocks':len({w['block'] for w in p['words']}),'words':len(p['words'])} for p in document['pages']]
        if key=='11':return line_table(source)
        if key=='12':
            from pypdf import PdfReader
            return {k:v.get('/V') for k,v in PdfReader(ROOT/'data/form.pdf').get_fields().items()}
        if key=='13':return extract(source,document)[0]
        if key=='14':return {'missing':decide(False,False,False,.99),'contradicted':decide(True,False,True,.99),'accepted':decide(True,True,True,.95)}
        if key=='15':return {'paired':contrastive_loss([[1,0],[0,1]]),'swapped':contrastive_loss([[0,1],[1,0]]),'kind':'paired-vector teaching algebra, not CLIP training'}
        if key=='16':return {'maxsim':maxsim([[1,0],[0,1]],[[1,0],[0,1]]),'kind':'handmade vectors, not learned page embeddings'}
        if key in ('17','18'):
            names=['openai'] if key=='17' else ['gemini','claude'];return {n:{'endpoint':request_spec(n,'explicit-model-required',source)['url'],'mode':'dry-run; no credential read'} for n in names}
        if key=='19':return answer_total(document,'tenant-a','Total')
        if key=='20':
            e=evidence_for(source,0,'Total: 47.25');e['bbox']=[1.,1.,30.,30.]
            try:validate_evidence(document,e)
            except ValueError:return {'unrelated_box_rejected':True}
            raise AssertionError('Bad evidence accepted')
        if key=='21':return {'allowed_hits':len(lexical_search('total',chunks(document,'a'),'a')),'other_tenant_hits':len(lexical_search('total',chunks(document,'a'),'b'))}
        if key=='22':return fuse([['page-a','page-b'],['page-b','page-c']])
        if key=='23':return prf(8,2,1)
        if key=='24':return risk_coverage([.99,.95,.6,.2],[False,True,True,False],.9)
        if key=='25':
            try:inspect_pdf(source,max_pages=1)
            except ValueError:return {'page_budget_rejected':True}
            raise AssertionError('Budget ignored')
        if key=='26':
            out=work/'redacted.pdf';redact_demo(source,out);return {'email_removed':all('demo@example.test' not in t for t in compare_text(out)),'scope':'synthetic native-text field; not a general PDF sanitization proof'}
        if key=='27':
            info=audio_info(ROOT/'data/tones.wav');segments=json.loads((ROOT/'data/transcript.json').read_text())['segments'];aligned_segments(segments,info['duration_ms']);return {'audio':info,'at_boundary':segment_at(segments,1500),'notice':'tones are not speech; transcript is manually authored'}
        if key=='28':return gif_frames(ROOT/'data/timeline.gif')
        if key in ('29','30','31','32'):
            if key=='30':
                try:process(source,work,'after_artifacts')
                except RuntimeError:pass
                assert not (work/'current.json').exists()
            result=process(source,work)
            if key=='31':
                target=work/'versions'/result['version']/'invoice.json';target.write_text('{}')
                try:read_current(work)
                except ValueError:return {'tampering_rejected':True}
                raise AssertionError('Tampering ignored')
            again=process(source,work) if key=='32' else read_current(work)
            return {'version':result['version'],'files':len(again['files']),'total_cents':json.loads((work/'versions'/result['version']/'invoice.json').read_text())['total_cents'],'repeat_stable':result==again}
    raise ValueError('Unknown lab')
def main(key=None):
    if key is None:
        p=argparse.ArgumentParser(description=__doc__);p.add_argument('lab',nargs='?');p.add_argument('--list',action='store_true');a=p.parse_args()
        if a.list:
            for k,v in LABS.items():print(k,v)
            return
        if not a.lab:p.error('Choose a lab or --list')
        key=a.lab.zfill(2)
    print(json.dumps({'lab':key,'goal':LABS[key],'result':run_lab(key)},ensure_ascii=False,indent=2,default=str))
if __name__=='__main__':main()

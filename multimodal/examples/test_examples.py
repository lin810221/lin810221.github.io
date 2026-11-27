import copy,json,math,unittest
from pathlib import Path
from unittest.mock import patch
from fixtures import ROOT
from geometry import box,iou,normalize,pixels,restore_crop,rotate_clockwise,tiles
from metrics import edit_distance,cer,anls,prf,cosine,maxsim,contrastive_loss,risk_coverage
from documents import inspect_pdf,compare_text,line_table,reading_order,redact_demo,evidence_for,validate_evidence
from contracts import Invoice,cents,decide
from pipeline import process,read_current,extract,writer_lock
from providers import request_spec,send,extract_text
from retrieval import chunks,lexical_search,fuse,answer_total
from media import audio_info,aligned_segments,segment_at,gif_frames
from run_lab import LABS,run_lab,scratch
SOURCE=ROOT/'data/invoice.pdf'
class GeometryTests(unittest.TestCase):
    def test_iou_disjoint_identical_overlap(self):
        self.assertEqual(iou([0,0,2,2],[3,3,4,4]),0);self.assertEqual(iou([0,0,2,2],[0,0,2,2]),1);self.assertAlmostEqual(iou([0,0,2,2],[1,1,3,3]),1/7)
    def test_invalid_box(self):
        for b in [[0,0,0,1],[-1,0,2,2],[0,0,float('nan'),2],[True,0,2,2]]:
            with self.assertRaises(ValueError):box(b)
    def test_normalize(self):self.assertEqual(normalize([10,20,30,40],100,200),(.1,.1,.3,.2))
    def test_point_pixel_scale(self):self.assertEqual(pixels([72,72,144,144],144),(144,144,288,288))
    def test_inverse_crop(self):self.assertEqual(restore_crop([20,30,80,90],[100,200],2),(110,215,140,245))
    def test_rotation(self):self.assertEqual(rotate_clockwise([10,20,50,80],612,792),(712,10,772,50))
    def test_tiling_coverage(self):
        r=tiles(1200,800);self.assertEqual(len(r),6);self.assertEqual(max(x[2] for x in r),1200);self.assertEqual(max(x[3] for x in r),800)
    def test_tiling_boundaries(self):
        self.assertEqual(tiles(100,80),[(0,0,100,80)])
        with self.assertRaises(ValueError):tiles(100,80,64,64)
class MetricTests(unittest.TestCase):
    def test_edit_operations(self):self.assertEqual(edit_distance('kitten','sitting'),3)
    def test_cer_can_exceed_one(self):self.assertEqual(cer('A','AAAA'),3)
    def test_empty_cer(self):self.assertIsNone(cer('',''))
    def test_anls_strict_boundary(self):self.assertEqual(anls('AB','AC'),0);self.assertAlmostEqual(anls('ABC','ABD'),2/3)
    def test_anls_empty(self):self.assertEqual(anls('',''),1);self.assertEqual(anls('','x'),0)
    def test_prf(self):self.assertAlmostEqual(prf(8,2,1)['f1'],16/19)
    def test_prf_empty(self):self.assertEqual(prf(0,0,0),{'precision':None,'recall':None,'f1':None})
    def test_cosine(self):self.assertEqual(cosine([1,0],[0,1]),0)
    def test_zero_vector(self):
        with self.assertRaises(ValueError):cosine([0,0],[1,2])
    def test_maxsim(self):self.assertEqual(maxsim([[1,0],[0,1]],[[1,0],[0,1]]),2)
    def test_contrastive_matching(self):self.assertLess(contrastive_loss([[1,0],[0,1]]),contrastive_loss([[0,1],[1,0]]))
    def test_extreme_logits_stay_finite(self):self.assertTrue(math.isfinite(contrastive_loss([[1,0],[0,1]],1e-5)))
    def test_risk_empty_selection(self):self.assertEqual(risk_coverage([.1],[True],.9),{'coverage':0,'risk':None})
class DocumentTests(unittest.TestCase):
    def test_native_and_scan(self):self.assertTrue(inspect_pdf(SOURCE)['pages'][0]['native_text']);self.assertFalse(inspect_pdf(ROOT/'data/scan.pdf')['pages'][0]['native_text'])
    def test_pypdf_comparison(self):self.assertIn('47.25',compare_text(SOURCE)[0])
    def test_native_table(self):self.assertEqual(line_table(SOURCE)[0]['cells'][1],['Cable','2','12.50','25.00'])
    def test_page_budget(self):
        with self.assertRaises(ValueError):inspect_pdf(SOURCE,max_pages=1)
    def test_file_type(self):
        with self.assertRaises(ValueError):inspect_pdf(ROOT/'data/scan.png')
    def test_rotated_page_metadata(self):self.assertEqual(inspect_pdf(ROOT/'data/rotated.pdf')['pages'][0]['rotation'],90)
    def test_valid_evidence(self):self.assertTrue(validate_evidence(inspect_pdf(SOURCE),evidence_for(SOURCE,0,'Total: 47.25')))
    def test_wrong_page_evidence(self):
        e=evidence_for(SOURCE,0,'Total: 47.25');e['page_index']=1
        with self.assertRaises(ValueError):validate_evidence(inspect_pdf(SOURCE),e)
    def test_wrong_region_evidence(self):
        e=evidence_for(SOURCE,0,'Total: 47.25');e['bbox']=[0,0,20,20]
        with self.assertRaises(ValueError):validate_evidence(inspect_pdf(SOURCE),e)
    def test_actual_redaction(self):
        with scratch() as root:
            redact_demo(SOURCE,root/'redacted.pdf');self.assertNotIn('demo@example.test',compare_text(root/'redacted.pdf')[0]);self.assertIn('demo@example.test',compare_text(SOURCE)[0])
class ContractTests(unittest.TestCase):
    def test_exact_cents(self):self.assertEqual(cents('47.25'),4725)
    def test_invalid_cents(self):
        for value in ['NaN','-1','1.234',1.2,True]:
            with self.assertRaises(ValueError):cents(value)
    def test_valid_invoice(self):self.assertEqual(extract(SOURCE,inspect_pdf(SOURCE))[0]['total_cents'],4725)
    def test_reconciliation(self):
        value=extract(SOURCE,inspect_pdf(SOURCE))[0];value['total_cents']=4726
        with self.assertRaises(ValueError):Invoice.model_validate(value)
    def test_evidence_coverage(self):
        value=extract(SOURCE,inspect_pdf(SOURCE))[0];del value['evidence']['currency']
        with self.assertRaises(ValueError):Invoice.model_validate(value)
    def test_bool_not_money(self):
        value=extract(SOURCE,inspect_pdf(SOURCE))[0];value['tax_cents']=True
        with self.assertRaises(ValueError):Invoice.model_validate(value)
    def test_high_confidence_does_not_override_missing_evidence(self):self.assertEqual(decide(True,False,True,.99),'review');self.assertEqual(decide(False,False,False,.99),'unknown')
class ProviderTests(unittest.TestCase):
    def test_pdf_payloads_use_provider_specific_shapes(self):
        a=request_spec('openai','explicit-model',SOURCE);self.assertIn('input_file',json.dumps(a));self.assertEqual(a['body']['text']['format']['type'],'json_schema')
        g=request_spec('gemini','explicit-model',SOURCE);self.assertTrue(g['url'].endswith('/v1/interactions'));self.assertIn('response_format',g['body'])
        c=request_spec('claude','explicit-model',SOURCE);self.assertIn('output_config',c['body'])
    def test_no_network_without_explicit_flag(self):
        with patch('providers.urlopen',side_effect=AssertionError('Network called')):
            with self.assertRaises(RuntimeError):send(request_spec('openai','explicit-model',SOURCE),'openai')
        from transcribe import prepare,transcribe
        spec=prepare(ROOT/'data/tones.wav','explicit-model')
        self.assertIn(b'name="file"',spec['body'])
        with patch('transcribe.urlopen',side_effect=AssertionError('Unexpected audio upload')):
            with self.assertRaises(RuntimeError):transcribe(spec)
    def test_unknown_provider(self):
        with self.assertRaises(ValueError):request_spec('unknown','model',SOURCE)
    def test_response_completion_and_schema(self):
        self.assertEqual(extract_text('openai',{'status':'completed','output':[{'content':[{'type':'output_text','text':'{"invoice_number":null,"total_text":"47.25"}'}]}]})['total_text'],'47.25')
        self.assertEqual(extract_text('gemini',{'status':'completed','steps':[{'type':'user_input','content':[{'type':'text','text':'not JSON'}]},{'type':'model_output','content':[{'type':'text','text':'{"invoice_number":null,"total_text":"47.25"}'}]}]})['total_text'],'47.25')
    def test_refusal_is_not_empty_success(self):
        with self.assertRaises(ValueError):extract_text('openai',{'status':'completed','output':[{'content':[{'type':'refusal'}]}]})
    def test_truncation(self):
        with self.assertRaises(ValueError):extract_text('claude',{'stop_reason':'max_tokens','content':[{'type':'text','text':'{}'}]})
class RetrievalMediaTests(unittest.TestCase):
    def test_permission_before_scoring(self):self.assertEqual(lexical_search('total',chunks(inspect_pdf(SOURCE),'a'),'b'),[])
    def test_known_and_unknown_answers(self):self.assertEqual(answer_total(inspect_pdf(SOURCE),'a','total')['answer'],'47.25');self.assertIsNone(answer_total(inspect_pdf(SOURCE),'a','bank account')['answer'])
    def test_fusion(self):self.assertEqual(fuse([['a','b'],['b','c']])[0][0],'b')
    def test_audio_duration(self):self.assertEqual(audio_info(ROOT/'data/tones.wav')['frames'],48000)
    def test_transcript_boundary(self):
        segments=json.loads((ROOT/'data/transcript.json').read_text())['segments'];aligned_segments(segments,3000);self.assertEqual(segment_at(segments,1500)[0]['text'],'Confirm total.');self.assertEqual(segment_at(segments,3000),[])
    def test_gif_timing(self):
        self.assertEqual(gif_frames(ROOT/'data/timeline.gif')[-1]['end_ms'],2000)
        from ffmpeg_frame import plan,execute
        with scratch() as w:
            command=plan(ROOT/'data/timeline.gif',w/'frame.png',.5)
            self.assertIn('-nostdin',command)
            with patch('ffmpeg_frame.subprocess.run',side_effect=AssertionError('Unexpected subprocess')):
                with self.assertRaises(RuntimeError):execute(command)
class PipelineTests(unittest.TestCase):
    def test_real_artifacts_and_replay(self):
        with scratch() as w:
            m=process(SOURCE,w);self.assertEqual(m,process(SOURCE,w));self.assertEqual(read_current(w),m);self.assertEqual(len(list((w/'versions').iterdir())),1)
    def test_failure_recovery(self):
        with scratch() as w:
            with self.assertRaises(RuntimeError):process(SOURCE,w,'after_artifacts')
            self.assertFalse((w/'current.json').exists());self.assertEqual(process(SOURCE,w),read_current(w))
    def test_tampering(self):
        with scratch() as w:
            m=process(SOURCE,w);(w/'versions'/m['version']/'invoice.json').write_text('{}')
            with self.assertRaises(ValueError):read_current(w)
    def test_path_traversal_pointer(self):
        with scratch() as w:
            m=process(SOURCE,w);m['version']='../../outside';(w/'current.json').write_text(json.dumps(m))
            with self.assertRaises(ValueError):read_current(w)
    def test_lock_rejects_second_writer(self):
        with scratch() as w:
            with writer_lock(w):
                with self.assertRaises(FileExistsError):process(SOURCE,w)
            self.assertFalse((w/'writer.lock').exists())
    def test_scan_not_guessed(self):
        with scratch() as w:
            with self.assertRaises(ValueError):process(ROOT/'data/scan.pdf',w)
            self.assertFalse((w/'current.json').exists())
    def test_html_contains_actual_source_and_escaped_fields(self):
        with scratch() as w:
            m=process(SOURCE,w);s=(w/'versions'/m['version']/'review.html').read_text();self.assertIn('page-0.png',s);self.assertIn('4725',s);self.assertIn('Total:',s)
    def test_all_32_entry_behaviors(self):
        self.assertEqual(len(LABS),32)
        with patch('urllib.request.urlopen',side_effect=AssertionError('Unexpected network')),patch('requests.sessions.Session.request',side_effect=AssertionError('Unexpected network')):
            for key in LABS:
                with self.subTest(lab=key):self.assertIsNotNone(run_lab(key))
if __name__=='__main__':unittest.main()

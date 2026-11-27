"""Portable document fixtures, source parity and study evidence."""
import json,re,posixpath,unittest
from pathlib import Path,PurePosixPath
from zipfile import ZipFile
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];C=R/'multimodal'
class MultimodalMaterialsTests(unittest.TestCase):
    def test_complete_original_units_and_diagrams(self):
        c=json.loads((C/'course.json').read_text(encoding='utf-8'));self.assertEqual((len(c['groups']),len(c['lessons']),len(c['visuals'])),(16,96,32))
        self.assertEqual(len({x['visualTask'] for x in c['lessons']}),96)
        for l in c['lessons']:
            s=(C/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8');self.assertGreater(len(s),1000);self.assertIn(l['visualTask'],s);self.assertNotIn('??',s)
    def test_complete_binary_fixtures_and_example_archive(self):
        with ZipFile(C/'examples.zip') as z:
            self.assertIsNone(z.testzip());names=set(z.namelist())
            for f in ['data/invoice.pdf','data/scan.pdf','data/rotated.pdf','data/form.pdf','data/scan.png','data/tones.wav','data/timeline.gif','data/transcript.json','pipeline.py','ocr_local.py','providers.py','contracts.py','test_examples.py','requirements-lock.txt','README.md','RUNBOOK.md','VERIFICATION.md','DATA_DICTIONARY.md']:
                self.assertIn('examples/'+f,names)
            self.assertEqual(len([n for n in names if re.fullmatch(r'examples/lab\d\d\.py',n)]),32)
            for n in names:
                self.assertNotIn('..',PurePosixPath(n).parts);self.assertNotIn('.runtime',PurePosixPath(n).parts);self.assertFalse(n.endswith('.onnx'));self.assertEqual(z.read(n),(C/n).read_bytes())
    def test_portable_study_pack_and_accessibility(self):
        with ZipFile(C/'study-pack.zip') as z:
            self.assertIsNone(z.testzip());names=set(z.namelist());self.assertEqual(len([n for n in names if n.endswith('.svg')]),32)
            for f in ['worksheet.md','answers.md']:self.assertEqual(len(re.findall(r'^## ',z.read('study-pack/study/'+f).decode('utf-8'),re.M)),96)
            self.assertEqual(len(re.findall(r'^## ',z.read('study-pack/study/glossary.md').decode('utf-8'),re.M)),115)
            for n in names:
                self.assertEqual(z.read(n),(C/n.removeprefix('study-pack/')).read_bytes())
                if n.endswith('.svg'):
                    el=ET.fromstring(z.read(n));self.assertEqual(el.attrib['role'],'img');self.assertTrue(el.attrib['aria-labelledby']);self.assertTrue(el.find('{http://www.w3.org/2000/svg}title').text);self.assertTrue(el.find('{http://www.w3.org/2000/svg}desc').text)
                if n.endswith('.md'):
                    for link in re.findall(r'\]\(([^)]+)\)',z.read(n).decode('utf-8')):
                        if '://' not in link and not link.startswith('#'):self.assertIn(posixpath.normpath(posixpath.join(posixpath.dirname(n),link)),names)
    def test_version_pins_models_and_quantitative_topics(self):
        v=json.loads((C/'study/versions.json').read_text(encoding='utf-8'));self.assertEqual(v['python'],'3.14.10');self.assertEqual(v['checked'],'2026-11-27');self.assertEqual(v['core_tests'],58)
        lock=(C/'examples/requirements-lock.txt').read_text(encoding='utf-8').lower()
        for k,version in v['packages'].items():self.assertIn(k.lower()+'=='+version,lock)
        self.assertEqual(len(v['models']),3)
        for digest in v['models'].values():self.assertRegex(digest,r'^[a-f0-9]{64}$')
        coverage=json.loads((R/'tools/math-topic-coverage.json').read_text(encoding='utf-8'))['courses']['multimodal']['formulaSections']
        for lid in ['008-dpi-coordinates','023-ocr-error-metrics','044-contrastive-objective','064-late-interaction','068-anls','071-risk-coverage','091-resource-limits']:self.assertIn(lid,coverage)
if __name__=='__main__':unittest.main()

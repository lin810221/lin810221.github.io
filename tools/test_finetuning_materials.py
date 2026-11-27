"""Editable source, quantitative definitions, real entrypoints and portable bundles."""
import hashlib,json,re,unittest,posixpath,xml.etree.ElementTree as ET
from pathlib import Path,PurePosixPath
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[1];COURSE=ROOT/'finetuning'
class FineTuningMaterialsTests(unittest.TestCase):
    def test_catalog_sources_figures_and_tasks(self):
        c=json.loads((COURSE/'course.json').read_text(encoding='utf-8'))
        self.assertEqual((len(c['groups']),len(c['lessons']),len(c['visuals'])),(12,72,24))
        self.assertEqual(c['updated'],'2026-11-25')
        self.assertEqual(len({l['visualTask'] for l in c['lessons']}),72)
        for lesson in c['lessons']:
            s=(COURSE/'chapters'/f'{lesson["id"]}.md').read_text(encoding='utf-8')
            self.assertIn(lesson['visualTask'],s);self.assertGreater(len(s),1000)
            self.assertNotIn('??',s)
        for f in c['visuals']:
            r=ET.fromstring((COURSE/f['file']).read_text(encoding='utf-8'))
            self.assertEqual(r.attrib['role'],'img')
            self.assertTrue(r.find('{http://www.w3.org/2000/svg}title').text)
            self.assertTrue(r.find('{http://www.w3.org/2000/svg}desc').text)

    def test_downloads_match_current_sources(self):
        with ZipFile(COURSE/'examples.zip') as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(len([n for n in z.namelist() if re.fullmatch(r'examples/\d\d_[^/]+\.py',n)]),24)
            for file in ['finetune_core.py','train_local.py','test_examples.py','VERIFICATION.md','requirements-lock.txt']:
                self.assertIn('examples/'+file,z.namelist())
            for name in z.namelist():
                self.assertNotIn('..',PurePosixPath(name).parts)
                self.assertNotIn('outputs',PurePosixPath(name).parts)
                self.assertNotIn('finetuning-output',PurePosixPath(name).parts)
                self.assertEqual(z.read(name),(COURSE/name).read_bytes())

    def test_study_bundle_covers_every_unit(self):
        with ZipFile(COURSE/'study-pack.zip') as z:
            self.assertIsNone(z.testzip());names=set(z.namelist())
            for file in ['worksheet.md','answers.md']:
                s=z.read('study-pack/study/'+file).decode('utf-8')
                self.assertEqual(len(re.findall(r'^## ',s,re.M)),72)
            s=z.read('study-pack/study/glossary.md').decode('utf-8')
            self.assertEqual(len(re.findall(r'^## ',s,re.M)),91)
            self.assertEqual(len([n for n in names if n.endswith('.svg')]),24)
            for name in names:
                if name.endswith('.svg'):
                    self.assertEqual(z.read(name),(COURSE/name.removeprefix('study-pack/')).read_bytes())
                if not name.endswith('.md'):continue
                for link in re.findall(r'\]\(([^)]+)\)',z.read(name).decode('utf-8')):
                    if '://' in link or link.startswith('#'):continue
                    self.assertIn(posixpath.normpath(posixpath.join(posixpath.dirname(name),link)),names)

    def test_version_pins_and_key_topic_definitions(self):
        v=json.loads((COURSE/'study/versions.json').read_text(encoding='utf-8'))
        self.assertEqual(v['checked'],'2026-11-25')
        pins=(COURSE/'examples/requirements.txt').read_text(encoding='utf-8')
        for k,version in v['packages'].items():self.assertIn(k+'=='+version,pins)
        coverage=json.loads((ROOT/'tools/math-topic-coverage.json').read_text(encoding='utf-8'))['courses']['finetuning']
        for lesson in ['014-autoregressive-loss','015-assistant-mask','025-lora-matrices','026-lora-gradients',
                       '037-gradient-accumulation','044-sequence-scores','045-dpo-objective','050-distillation']:
            self.assertIn(lesson,coverage['formulaSections'])
if __name__=='__main__':unittest.main()

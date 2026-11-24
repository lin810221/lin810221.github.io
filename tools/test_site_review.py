"""Publishing gates covering the four failures found in the 2026-11-24 review."""
import json,re,unittest,posixpath
from pathlib import Path
from zipfile import ZipFile
from build import assert_readable
from validate import InspectHTML
ROOT=Path(__file__).resolve().parents[1]

class SiteReviewTests(unittest.TestCase):
    def test_every_unit_has_a_local_accessible_diagram(self):
        for path in ROOT.glob('*/course.json'):
            c=json.loads(path.read_text(encoding='utf-8'));figures={f['id']:f for f in c.get('visuals',[])}
            self.assertTrue(figures,path.parent.name)
            for lesson in c['lessons']:
                with self.subTest(course=path.parent.name,unit=lesson['id']):
                    self.assertIn(lesson.get('visual'),figures)
                    source=(path.parent/'chapters'/f'{lesson["id"]}.md').read_text(encoding='utf-8')
                    self.assertIn(figures[lesson['visual']]['file'],source)
                    if 'visualTask' in lesson:
                        self.assertGreater(len(lesson['visualTask']),20)
                    else:
                        # Anatomy predates the metadata field; its task is editable prose.
                        task=re.search(r'## 先讀這張圖\n(.*?)(?=\n## |\Z)',source,re.S)
                        self.assertIsNotNone(task)
                        prose=re.sub(r'<[^>]+>','',task[1])
                        self.assertGreater(len(re.findall(r'[\u4e00-\u9fff]',prose)),30)

    def test_all_published_equations_are_prerendered(self):
        for path in ROOT.glob('*/assets/course-data.js'):
            c=json.loads(path.read_text(encoding='utf-8').split('window.COURSE = ',1)[1].strip().removesuffix(';'))
            self.assertTrue(c.get('mathRenderer',{}).get('prerendered'),path)
            for l in c['lessons']:
                with self.subTest(course=c.get('slug',path.parents[1].name),unit=l['id']):
                    h=l['html']+l.get('summaryHTML','')
                    count=len(re.findall(r' data-tex="',h))
                    self.assertEqual(count,len(re.findall(r' data-rendered="katex"',h)))
                    self.assertEqual(count,h.count('class="katex"'))
                    self.assertNotIn('class="katex-error"',h)
                    self.assertNotIn('data-math-error',h)
                    self.assertEqual(count,h.count('encoding="application/x-tex"'))

    def test_no_corrupted_sources_catalogs_study_or_figures(self):
        for catalog in ROOT.glob('*/course.json'):
            folder=catalog.parent
            for p in [catalog,*sorted((folder/'chapters').glob('*.md')),*sorted((folder/'study').glob('*.md')),*sorted((folder/'assets/figures').glob('*.svg'))]:
                # unicode is decoded strictly; prose additionally rejects already-lost ASCII runs.
                assert_readable(p.read_text(encoding='utf-8'),str(p))

    def test_restored_transformer_unit_is_chinese_and_specific(self):
        p=ROOT/'transformer/chapters/065-hybrids.md';s=p.read_text(encoding='utf-8')
        self.assertGreater(len(re.findall(r'[\u4e00-\u9fff]',s)),600)
        for term in ['SSM','Attention','131072','SFT','4096']:self.assertIn(term,s)

    def test_new_chapter_study_packs_have_current_assets_and_portable_links(self):
        for path in ROOT.glob('*/course.json'):
            c=json.loads(path.read_text(encoding='utf-8'))
            if c.get('visualPresentation')!='chapter':continue
            with ZipFile(path.parent/c['studyBundle']) as z:
                self.assertIsNone(z.testzip());names=set(z.namelist())
                for f in c['visuals']:
                    name='study-pack/'+f['file'];self.assertIn(name,names)
                    self.assertEqual(z.read(name),(path.parent/f['file']).read_bytes())
                for name in names:
                    if not name.endswith('.md'):continue
                    for link in re.findall(r'\]\(([^)]+)\)',z.read(name).decode('utf-8')):
                        if '://' in link or link.startswith('#'):continue
                        self.assertIn(posixpath.normpath(posixpath.join(posixpath.dirname(name),link)),names,(name,link))

if __name__=='__main__':unittest.main()

"""Read-only checks for visual learning, SVG access and standalone worksheets."""
import csv
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import re
import unittest
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET
import zipfile

ROOT=Path(__file__).resolve().parents[1]
COURSE=ROOT/'anatomy-physiology'
CATALOG=json.loads((COURSE/'course.json').read_text(encoding='utf-8'))
SVG='{http://www.w3.org/2000/svg}'

class VisualLearningTests(unittest.TestCase):
    def test_scope(self):
        self.assertEqual(len(CATALOG['groups']),20)
        self.assertEqual(len(CATALOG['lessons']),120)
        self.assertEqual(len(CATALOG['visuals']),64)
    def test_six_units_in_each_chapter(self):
        self.assertEqual([sum(l['group']==g['id'] for l in CATALOG['lessons']) for g in CATALOG['groups']],[6]*20)
    def test_no_required_code_environment(self):
        self.assertNotIn('exampleBundle',CATALOG)
        self.assertFalse(any(l.get('example') for l in CATALOG['lessons']))
        self.assertFalse((COURSE/'examples').exists())
    def test_every_unit_has_relevant_visual(self):
        figures={f['id']:f for f in CATALOG['visuals']}
        for l in CATALOG['lessons']:
            with self.subTest(unit=l['id']):
                self.assertEqual(figures[l['visual']]['group'],l['group'])
                body=(COURSE/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
                self.assertIn(figures[l['visual']]['file'],body)
                for extra in l.get('extraVisuals',[]):self.assertIn(figures[extra]['file'],body)
    def test_all_64_figures_used_in_teaching(self):
        used={l['visual'] for l in CATALOG['lessons']}
        used.update(f for l in CATALOG['lessons'] for f in l.get('extraVisuals',[]))
        self.assertEqual(used,{f['id'] for f in CATALOG['visuals']})
    def test_each_unit_has_life_case_and_answer(self):
        for l in CATALOG['lessons']:
            body=(COURSE/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
            self.assertIn('## 放回生活情境',body)
            self.assertIn('## 不寫程式的自我檢核',body)
            self.assertIn('<details>',body)
            self.assertNotIn('```python',body)
    def test_image_alternative_text_and_enlarge_links(self):
        for l in CATALOG['lessons']:
            body=(COURSE/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
            alts=re.findall(r'<img [^>]*alt="([^"]+)"',body)
            self.assertTrue(alts)
            self.assertTrue(all(len(a)>20 for a in alts))
            self.assertIn('target="_blank" rel="noopener"',body)
    def test_svg_titles_descriptions_and_identifiers(self):
        for f in CATALOG['visuals']:
            with self.subTest(figure=f['id']):
                tree=ET.parse(COURSE/f['file']);root=tree.getroot()
                self.assertEqual(root.tag,SVG+'svg')
                self.assertEqual(root.attrib['role'],'img')
                self.assertTrue(root.find(SVG+'title').text)
                self.assertGreater(len(root.find(SVG+'desc').text),20)
                ids=[el.attrib['id'] for el in root.iter() if 'id' in el.attrib]
                self.assertEqual(len(ids),len(set(ids)))
                self.assertTrue(set(root.attrib['aria-labelledby'].split())<=set(ids))
    def test_no_svg_scripts_or_remote_dependencies(self):
        for f in CATALOG['visuals']:
            root=ET.parse(COURSE/f['file']).getroot()
            for el in root.iter():
                self.assertNotEqual(el.tag,SVG+'script')
                self.assertFalse(any(k.lower().startswith('on') for k in el.attrib))
                for k,v in el.attrib.items():
                    if k.endswith('href'):self.assertFalse(v.startswith(('http:','https:','//')))
    def test_figure_coordinates_and_labels_within_canvas(self):
        for f in CATALOG['visuals']:
            root=ET.parse(COURSE/f['file']).getroot()
            for el in root.findall('.//'+SVG+'text'):
                with self.subTest(figure=f['id'],label=el.text):
                    self.assertTrue(0<=float(el.attrib['x'])<860)
                    self.assertTrue(0<=float(el.attrib['y'])<510)
    def test_direction_and_boundary_notes(self):
        bodies='\n'.join((COURSE/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8') for l in CATALOG['lessons'])
        for term in ['人體右','非比例','濾液不是','動脈離心','母體與胎兒','尿道口和陰道口']:
            self.assertIn(term,bodies)
    def test_worksheets_cover_all_units(self):
        for name in ['workbook.md','answers.md']:
            body=(COURSE/'study'/name).read_text(encoding='utf-8')
            self.assertEqual(len(re.findall(r'^### 單元 ',body,re.M)),120)
            for lesson in CATALOG['lessons']:self.assertIn(lesson['title'],body)
    def test_bilingual_glossary(self):
        rows=list(csv.DictReader(io.StringIO((COURSE/'study/glossary.csv').read_text(encoding='utf-8-sig'))))
        self.assertEqual(len(rows),100)
        self.assertEqual(len({r['中文'] for r in rows}),100)
        self.assertTrue(all(r['English'] and r['學習用簡釋'] for r in rows))
    def test_source_dates_and_attribution(self):
        body=(COURSE/'study/sources.md').read_text(encoding='utf-8')
        for word in ['2026-11-16','不是出版日','第三方','403','405','2010']:
            self.assertIn(word,body)
        self.assertGreaterEqual(body.count('https://'),50)
    def test_resources_exist_within_course(self):
        for name in CATALOG['learningResources']:
            p=(COURSE/name).resolve()
            self.assertTrue(p.is_relative_to(COURSE.resolve()) and p.is_file())

class StudyBundleTests(unittest.TestCase):
    def setUp(self):self.bundle=zipfile.ZipFile(COURSE/CATALOG['studyBundle'])
    def tearDown(self):self.bundle.close()
    def test_standalone_member_layout(self):
        names=self.bundle.namelist()
        self.assertEqual(len(names),len(set(names)))
        self.assertEqual(sum(name.endswith('.svg') for name in names),64)
        self.assertTrue(all(name.startswith('study-pack/') and '..' not in PurePosixPath(name).parts for name in names))
        self.assertTrue(all(not name.endswith(('.py','.exe','.dll')) for name in names))
    def test_source_bytes_match_bundle(self):
        for name in self.bundle.namelist():
            relative=PurePosixPath(name).relative_to('study-pack')
            self.assertEqual(self.bundle.read(name),(COURSE/relative).read_bytes(),name)
    def test_markdown_links_work_inside_archive(self):
        names=set(self.bundle.namelist())
        for name in names:
            if not name.endswith('.md'):continue
            for link in re.findall(r'\]\(([^)]+)\)',self.bundle.read(name).decode('utf-8')):
                parsed=urlparse(link)
                if parsed.scheme or link.startswith('#'):continue
                parts=[]
                for p in (PurePosixPath(name).parent/PurePosixPath(unquote(parsed.path))).parts:
                    if p=='..':parts.pop()
                    elif p!='.':parts.append(p)
                self.assertIn('/'.join(parts),names,(name,link))
    def test_all_svg_files_parse_from_archive(self):
        for name in self.bundle.namelist():
            if name.endswith('.svg'):self.assertEqual(ET.fromstring(self.bundle.read(name)).tag,SVG+'svg')
    def test_original_diagrams_and_worksheets_available_without_website(self):
        for relative in ['study/README.md','study/workbook.md','study/answers.md','study/glossary.csv','study/sources.md']:
            self.assertIn('study-pack/'+relative,self.bundle.namelist())
    def test_download_integrity(self):self.assertIsNone(self.bundle.testzip())

class BundleBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('learning_build',ROOT/'tools/build.py')
        cls.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.module)
    def test_reject_bundle_path_escape(self):
        with self.assertRaises(ValueError):self.module.build_study_bundle(COURSE,{'studyBundle':'../outside.zip','studyFiles':['study']})
    def test_reject_resource_path_escape(self):
        with self.assertRaises(ValueError):self.module.build_study_bundle(COURSE,{'studyBundle':'unused-test.zip','studyFiles':['../README.md']})
    def test_reject_missing_source(self):
        with self.assertRaises(ValueError):self.module.build_study_bundle(COURSE,{'studyBundle':'unused-test.zip','studyFiles':['missing-study-source']})
    def test_reject_empty_bundle(self):
        with self.assertRaises(ValueError):self.module.build_study_bundle(COURSE,{'studyBundle':'unused-test.zip','studyFiles':[]})
    def test_legacy_course_without_study_bundle_is_untouched(self):
        self.module.build_study_bundle(ROOT/'ergonomics',{})
        self.assertFalse((ROOT/'ergonomics/unused-test.zip').exists())

if __name__=='__main__':unittest.main()

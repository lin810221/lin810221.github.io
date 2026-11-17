"""Evidence course learning materials, provenance, accessibility and offline integrity."""
import csv
import io
import json
from pathlib import Path,PurePosixPath
import posixpath
import re
import unittest
from urllib.parse import urlparse,unquote
import xml.etree.ElementTree as ET
import zipfile

ROOT=Path(__file__).resolve().parents[1];C=ROOT/'evidence-health'
SVG='{http://www.w3.org/2000/svg}'
CAT=json.loads((C/'course.json').read_text(encoding='utf-8'))

class EvidenceMaterialsTests(unittest.TestCase):
    def test_scope(self):
        self.assertEqual((len(CAT['groups']),len(CAT['lessons']),len(CAT['visuals'])),(18,108,54))
        self.assertEqual(len({l['id'] for l in CAT['lessons']}),108)
        self.assertTrue(all(l.get('summary') and isinstance(l.get('tags'),list) and l['tags'] for l in CAT['lessons']))
        self.assertEqual([sum(l['group']==g['id'] for l in CAT['lessons']) for g in CAT['groups']],[6]*18)
    def test_necessary_and_advanced_topics_are_present(self):
        titles=' '.join(l['title'] for l in CAT['lessons'])
        for term in ['PICO','隨機','失訪','不死時間','傾向分數','DAG','中介','NNT','HR','交互作用','自然頻率','過度診斷','RoB 2','森林圖','GRADE','指南','利益衝突','AI','專題']:
            self.assertIn(term,titles)
    def test_no_required_programming(self):
        self.assertNotIn('exampleBundle',CAT)
        self.assertFalse(any(l.get('example') for l in CAT['lessons']))
        self.assertFalse((C/'examples').exists())
    def test_figure_coverage(self):
        figures={f['id']:f for f in CAT['visuals']}
        self.assertEqual(len(figures),54)
        self.assertEqual([sum(f['group']==g['id'] for f in CAT['visuals']) for g in CAT['groups']],[3]*18)
        for l in CAT['lessons']:
            self.assertEqual(figures[l['visual']]['group'],l['group'])
            self.assertIn(l['id'],figures[l['visual']]['lessons'])
        self.assertEqual({l['visual'] for l in CAT['lessons']},set(figures))
    def test_substantive_individual_lessons(self):
        tasks=[]
        for l in CAT['lessons']:
            text=(C/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
            self.assertGreater(len(re.findall(r'[\u4e00-\u9fff]',text)),650,l['id'])
            self.assertIn('## 放進研究情境',text)
            self.assertIn('## 常見誤讀與修正',text)
            self.assertIn('## 不寫程式的自我檢核',text)
            self.assertIn('<details><summary>',text)
            self.assertIn(l['visualTask'],text)
            self.assertGreater(len(l['visualTask']),35)
            tasks.append(l['visualTask'])
        self.assertEqual(len(set(tasks)),108)
    def test_zoomable_images_and_meaningful_alternatives(self):
        for l in CAT['lessons']:
            text=(C/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
            self.assertIn('target="_blank" rel="noopener"',text)
            self.assertGreater(len(re.search(r'<img [^>]*alt="([^"]+)"',text)[1]),25)
            self.assertEqual(text.count('<figure class="health-figure">'),1)
    def test_svg_accessibility_and_no_executables(self):
        for f in CAT['visuals']:
            with self.subTest(figure=f['id']):
                root=ET.parse(C/f['file']).getroot()
                self.assertEqual(root.tag,SVG+'svg');self.assertEqual(root.attrib['role'],'img')
                self.assertTrue(root.find(SVG+'title').text)
                self.assertGreater(len(root.find(SVG+'desc').text),25)
                ids=[el.attrib['id'] for el in root.iter() if 'id' in el.attrib]
                self.assertEqual(len(ids),len(set(ids)))
                self.assertTrue(set(root.attrib['aria-labelledby'].split())<=set(ids))
                for el in root.iter():
                    self.assertNotIn(el.tag,[SVG+'script',SVG+'image',SVG+'foreignObject'])
                    self.assertFalse(any(k.lower().startswith('on') for k in el.attrib))
                    for k,v in el.attrib.items():
                        if k.endswith('href'):self.assertFalse(v.startswith(('http:','https:','//','data:')))
    def test_figure_manifest_and_local_scope(self):
        self.assertEqual(json.loads((C/'assets/figures/manifest.json').read_text(encoding='utf-8')),CAT['visuals'])
        for f in CAT['visuals']:
            self.assertTrue((C/f['file']).resolve().is_relative_to(C.resolve()))
            self.assertGreater(len(f['note']),15)
            self.assertTrue(all(s['title'] and urlparse(s['url']).scheme=='https' for s in f['sources']))
    def test_workbook_and_answer_coverage(self):
        for name in ['workbook.md','answers.md']:
            text=(C/'study'/name).read_text(encoding='utf-8')
            self.assertEqual(len(re.findall(r'^### 單元 ',text,re.M)),108)
            for l in CAT['lessons']:self.assertIn(l['title'],text)
        self.assertEqual((C/'study/workbook.md').read_text(encoding='utf-8').count('[看圖：'),108)
    def test_bilingual_glossary(self):
        rows=list(csv.DictReader(io.StringIO((C/'study/glossary.csv').read_text(encoding='utf-8-sig'))))
        self.assertEqual(len(rows),120);self.assertEqual(len({r['中文'] for r in rows}),120)
        self.assertTrue(all(r['English'] and len(r['學習用簡釋'])>15 for r in rows))
    def test_synthetic_cases_keep_unknowns_and_units(self):
        data=json.loads((C/'study/cases.json').read_text(encoding='utf-8'))
        self.assertTrue(data['synthetic']);self.assertEqual(data['trial']['horizonMonths'],12)
        self.assertIsNone(data['trial']['protocolRecord']);self.assertIsNone(data['trial']['funding'])
        self.assertEqual(data['trial']['expected']['nntBenefitPoint'],100)
        self.assertEqual(data['attrition']['expectedRDExtremes'],[-.1,.05])
        self.assertEqual(sum(data['diagnosis']['expected'][k] for k in ['tp','fn','fp','tn']),data['diagnosis']['n'])
        self.assertIsNone(data['meta']['betweenStudyVariance'])
    def test_dates_drafts_and_access_limits_are_distinct(self):
        text=(C/'study/sources.md').read_text(encoding='utf-8')
        for term in ['2026-11-16','2025','2020','6.5.1','6.5／2024','草案','2016','IPDAS','GRADE','出版日']:
            self.assertIn(term,text)
        self.assertGreaterEqual(len(set(re.findall(r'https://[^)\s]+',text))),25)
    def test_resources_and_script_order(self):
        for rel in CAT['learningResources']:
            path=(C/rel).resolve();self.assertTrue(path.is_relative_to(C.resolve()) and path.is_file())
        page=(C/'index.html').read_text(encoding='utf-8')
        self.assertIn('../assets/health-visuals.css',page)
        self.assertLess(page.index('assets/course-data.js'),page.index('assets/overview.js'))
        self.assertLess(page.index('assets/overview.js'),page.index('../assets/reader.js'))

class EvidenceBundleTests(unittest.TestCase):
    def setUp(self):self.zip=zipfile.ZipFile(C/CAT['studyBundle'])
    def tearDown(self):self.zip.close()
    def test_complete_safe_standalone_bundle(self):
        names=self.zip.namelist()
        self.assertEqual(len(names),61);self.assertEqual(len(set(names)),61)
        self.assertEqual(sum(n.endswith('.svg') for n in names),54)
        self.assertTrue(all(n.startswith('study-pack/') and '..' not in PurePosixPath(n).parts for n in names))
        self.assertTrue(all(not n.endswith(('.py','.exe','.dll')) for n in names))
        self.assertIsNone(self.zip.testzip())
    def test_archive_bytes_equal_sources(self):
        for name in self.zip.namelist():
            relative=PurePosixPath(name).relative_to('study-pack')
            self.assertEqual(self.zip.read(name),(C/relative).read_bytes(),name)
    def test_markdown_links_resolve_inside_archive(self):
        names=set(self.zip.namelist())
        for name in names:
            if not name.endswith('.md'):continue
            for link in re.findall(r'\]\(([^)]+)\)',self.zip.read(name).decode('utf-8')):
                parsed=urlparse(link)
                if parsed.scheme or link.startswith('#'):continue
                target=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(parsed.path)))
                self.assertIn(target,names,(name,link))
    def test_svg_files_parse_from_bundle(self):
        for name in self.zip.namelist():
            if name.endswith('.svg'):self.assertEqual(ET.fromstring(self.zip.read(name)).tag,SVG+'svg')

if __name__=='__main__':unittest.main()

"""Read-only integrity checks for visual supplements and their offline bundles."""
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import unittest
from urllib.parse import unquote,urlparse
import xml.etree.ElementTree as ET
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SLUGS=['nutrition','exercise-science','metabolic-health','mental-health','ergonomics']
SVG='{http://www.w3.org/2000/svg}'

class HealthVisualTests(unittest.TestCase):
    def setUp(self):
        self.courses={slug:json.loads((ROOT/slug/'course.json').read_text(encoding='utf-8')) for slug in SLUGS}
    def test_scope_and_chapter_coverage(self):
        for slug,c in self.courses.items():
            with self.subTest(course=slug):
                self.assertEqual((len(c['groups']),len(c['lessons']),len(c['visuals'])),(16,96,48))
                self.assertEqual([sum(f['group']==g['id'] for f in c['visuals']) for g in c['groups']],[3]*16)
                self.assertEqual([sum(l['group']==g['id'] for l in c['lessons']) for g in c['groups']],[6]*16)
    def test_unique_complete_figure_mapping(self):
        for slug,c in self.courses.items():
            figures={f['id']:f for f in c['visuals']}
            self.assertEqual(len(figures),48)
            self.assertEqual(len({f['file'] for f in c['visuals']}),48)
            self.assertEqual({l['visual'] for l in c['lessons']},set(figures))
            for l in c['lessons']:
                self.assertEqual(figures[l['visual']]['group'],l['group'])
                self.assertEqual(sum(unit['visual']==l['visual'] for unit in c['lessons']),2)
    def test_unique_reading_tasks_per_unit(self):
        for slug,c in self.courses.items():
            self.assertEqual(len({l['visualTask'] for l in c['lessons']}),96)
            for l in c['lessons']:
                self.assertGreater(len(l['visualTask']),35)
                text=(ROOT/slug/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
                self.assertIn(l['visualTask'],text)
                self.assertEqual(text.count('<!-- health-visual:start -->'),1)
                self.assertEqual(text.count('<!-- health-visual:end -->'),1)
    def test_accessible_zoomable_lesson_images(self):
        for slug,c in self.courses.items():
            for l in c['lessons']:
                text=(ROOT/slug/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
                block=text.split('<!-- health-visual:start -->')[1].split('<!-- health-visual:end -->')[0]
                self.assertIn('target="_blank" rel="noopener"',block)
                self.assertGreater(len(re.search(r'<img [^>]*alt="([^"]+)"',block)[1]),20)
                self.assertIn('<figcaption>',block)
                self.assertIn('## 圖解閱讀 {#visual-reading}',block)
    def test_local_svg_titles_descriptions_and_no_executable_or_remote_content(self):
        for slug,c in self.courses.items():
            for f in c['visuals']:
                with self.subTest(course=slug,figure=f['id']):
                    path=(ROOT/slug/f['file']).resolve()
                    self.assertTrue(path.is_relative_to((ROOT/slug).resolve()))
                    root=ET.parse(path).getroot()
                    self.assertEqual(root.tag,SVG+'svg')
                    self.assertEqual(root.attrib['role'],'img')
                    self.assertTrue(root.find(SVG+'title').text)
                    self.assertGreater(len(root.find(SVG+'desc').text),20)
                    ids=[el.attrib['id'] for el in root.iter() if 'id' in el.attrib]
                    self.assertEqual(len(ids),len(set(ids)))
                    self.assertTrue(set(root.attrib['aria-labelledby'].split())<=set(ids))
                    for el in root.iter():
                        self.assertNotIn(el.tag,[SVG+'script',SVG+'foreignObject',SVG+'image'])
                        self.assertFalse(any(k.lower().startswith('on') for k in el.attrib))
                        for k,v in el.attrib.items():
                            if k.endswith('href'):self.assertFalse(v.startswith(('http:','https:','//','data:')))
    def test_manifest_matches_catalog_and_sources(self):
        for slug,c in self.courses.items():
            self.assertEqual(json.loads((ROOT/slug/'assets/figures/manifest.json').read_text(encoding='utf-8')),c['visuals'])
            for f in c['visuals']:
                self.assertTrue(f['sources'])
                self.assertTrue(all(urlparse(s['url']).scheme=='https' and s['title'] for s in f['sources']))
                self.assertGreater(len(f['note']),12)
                if f.get('reusedFrom'):self.assertTrue((ROOT/f['reusedFrom']).is_file())
    def test_reader_script_order_and_shared_styles(self):
        for slug in SLUGS:
            page=(ROOT/slug/'index.html').read_text(encoding='utf-8')
            self.assertIn('../assets/health-visuals.css',page)
            self.assertLess(page.index('assets/overview.js'),page.index('../assets/health-visuals.js'))
            self.assertLess(page.index('../assets/health-visuals.js'),page.index('../assets/reader.js'))
    def test_baseline_dates_and_original_examples_remain_available(self):
        for slug,c in self.courses.items():
            self.assertEqual(c['visualUpdated'],'2026-11-16')
            self.assertLess(c['contentBaselineDate'],c['visualUpdated'])
            self.assertEqual(c['exampleBundle'],'examples.zip')
            self.assertEqual(sum(bool(l.get('example')) for l in c['lessons']),48)
            self.assertTrue((ROOT/slug/'examples/README.md').is_file())
    def test_study_tasks_cover_all_units(self):
        for slug,c in self.courses.items():
            text=(ROOT/slug/'study/read-tasks.md').read_text(encoding='utf-8')
            self.assertEqual(len(re.findall(r'^### 單元 ',text,re.M)),96)
            for l in c['lessons']:self.assertIn(l['visualTask'],text)
    def test_learning_resources_are_local(self):
        for slug,c in self.courses.items():
            for relative in c['learningResources']:
                path=(ROOT/slug/relative).resolve()
                self.assertTrue(path.is_relative_to((ROOT/slug).resolve()) and path.is_file())
    def test_study_bundle_matches_source_and_stands_alone(self):
        for slug,c in self.courses.items():
            with zipfile.ZipFile(ROOT/slug/c['studyBundle']) as bundle:
                names=bundle.namelist();members=set(names)
                self.assertEqual(len(names),52)
                self.assertEqual(len(members),52)
                self.assertEqual(sum(n.endswith('.svg') for n in names),48)
                self.assertIsNone(bundle.testzip())
                for name in names:
                    self.assertTrue(name.startswith('study-pack/') and '..' not in PurePosixPath(name).parts)
                    relative=PurePosixPath(name).relative_to('study-pack')
                    self.assertEqual(bundle.read(name),(ROOT/slug/relative).read_bytes())
                    if name.endswith('.md'):
                        for link in re.findall(r'\]\(([^)]+)\)',bundle.read(name).decode('utf-8')):
                            parsed=urlparse(link)
                            if parsed.scheme or link.startswith('#'):continue
                            target=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(parsed.path)))
                            self.assertIn(target,members,(slug,name,link))
                    elif name.endswith('.svg'):ET.fromstring(bundle.read(name))

if __name__=='__main__':unittest.main()

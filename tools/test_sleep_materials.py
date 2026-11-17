"""Sleep curriculum accessibility, synthetic time definitions and offline integrity."""
import csv,io,json,re,posixpath,unittest,zipfile
from datetime import datetime,timedelta,timezone
from pathlib import Path,PurePosixPath
from urllib.parse import urlparse,unquote
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'sleep-science'
CAT=json.loads((C/'course.json').read_text(encoding='utf-8'));SVG='{http://www.w3.org/2000/svg}'
class SleepMaterialsTests(unittest.TestCase):
    def test_scope_and_reader_metadata(self):
        self.assertEqual((len(CAT['groups']),len(CAT['lessons']),len(CAT['visuals'])),(18,108,54))
        self.assertEqual(len({l['id'] for l in CAT['lessons']}),108)
        self.assertTrue(all(l.get('summary') and isinstance(l.get('tags'),list) and l['tags'] for l in CAT['lessons']))
        self.assertEqual([sum(l['group']==g['id'] for l in CAT['lessons']) for g in CAT['groups']],[6]*18)
    def test_core_and_advanced_topics(self):
        titles=' '.join(l['title'] for l in CAT['lessons'])
        for term in ['非快速動眼','REM','雙過程','SCN','分子時鐘','DLMO','相位反應','安全睡眠','睡眠中點','WASO','CBT-I','AHI','REI','輪班','時差','猝睡','REM睡眠行為','專題']:
            self.assertIn(term,titles)
        self.assertIn('NREM',(C/'chapters/008-nrem.md').read_text(encoding='utf-8'))
    def test_no_required_programming(self):
        self.assertNotIn('exampleBundle',CAT);self.assertFalse(any(l.get('example') for l in CAT['lessons']));self.assertFalse((C/'examples').exists())
    def test_all_units_have_relevant_figures(self):
        figures={f['id']:f for f in CAT['visuals']};self.assertEqual(len(figures),54)
        self.assertEqual([sum(f['group']==g['id'] for f in CAT['visuals']) for g in CAT['groups']],[3]*18)
        for l in CAT['lessons']:
            self.assertEqual(figures[l['visual']]['group'],l['group']);self.assertIn(l['id'],figures[l['visual']]['lessons'])
        self.assertEqual({l['visual'] for l in CAT['lessons']},set(figures))
    def test_individual_explanations_and_answers(self):
        tasks=[]
        for l in CAT['lessons']:
            text=(C/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
            self.assertGreater(len(re.findall(r'[\u4e00-\u9fff]',text)),650,l['id'])
            for term in ['## 核心概念與機制','## 放回生活與研究情境','## 不寫程式的自我檢核','<details><summary>']:self.assertIn(term,text)
            self.assertIn(l['visualTask'],text);self.assertGreater(len(l['visualTask']),35);tasks.append(l['visualTask'])
        self.assertEqual(len(set(tasks)),108)
    def test_zoomable_accessible_lesson_images(self):
        for l in CAT['lessons']:
            text=(C/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
            self.assertIn('target="_blank" rel="noopener"',text)
            self.assertEqual(text.count('<figure class="health-figure">'),1)
            self.assertGreater(len(re.search(r'<img [^>]*alt="([^"]+)"',text)[1]),25)
    def test_svg_accessibility_and_independent_assets(self):
        for f in CAT['visuals']:
            with self.subTest(figure=f['id']):
                root=ET.parse(C/f['file']).getroot();self.assertEqual(root.tag,SVG+'svg');self.assertEqual(root.attrib['role'],'img')
                self.assertTrue(root.find(SVG+'title').text);self.assertGreater(len(root.find(SVG+'desc').text),25)
                ids=[el.attrib['id'] for el in root.iter() if 'id' in el.attrib];self.assertEqual(len(ids),len(set(ids)))
                self.assertTrue(set(root.attrib['aria-labelledby'].split())<=set(ids))
                for el in root.iter():
                    self.assertNotIn(el.tag,[SVG+'script',SVG+'image',SVG+'foreignObject']);self.assertFalse(any(k.lower().startswith('on') for k in el.attrib))
                    for k,v in el.attrib.items():
                        if k.endswith('href'):self.assertFalse(v.startswith(('http:','https:','//','data:')))
    def test_manifest_and_attribution(self):
        self.assertEqual(json.loads((C/'assets/figures/manifest.json').read_text(encoding='utf-8')),CAT['visuals'])
        for f in CAT['visuals']:
            self.assertTrue((C/f['file']).resolve().is_relative_to(C.resolve()));self.assertGreater(len(f['note']),15)
            self.assertTrue(f['sources']);self.assertTrue(all(s['title'] and urlparse(s['url']).scheme=='https' for s in f['sources']))
    def test_workbook_and_answers(self):
        for name in ['workbook.md','answers.md']:
            text=(C/'study'/name).read_text(encoding='utf-8');self.assertEqual(len(re.findall(r'^### 單元 ',text,re.M)),108)
            for l in CAT['lessons']:self.assertIn(l['title'],text)
        self.assertEqual((C/'study/workbook.md').read_text(encoding='utf-8').count('[看圖：'),108)
    def test_bilingual_glossary(self):
        rows=list(csv.DictReader(io.StringIO((C/'study/glossary.csv').read_text(encoding='utf-8-sig'))))
        self.assertEqual(len(rows),120);self.assertEqual(len({r['中文'] for r in rows}),120)
        self.assertTrue(all(r['English'] and len(r['學習用簡釋'])>15 for r in rows))
    def test_synthetic_architecture_and_diary_are_distinct(self):
        d=json.loads((C/'study/cases.json').read_text(encoding='utf-8'));self.assertTrue(d['synthetic'])
        totals={k:sum(minutes for stage,minutes in d['architecture']['segments'] if stage==k) for k in ['W','N1','N2','N3','REM']}
        self.assertEqual(sum(totals.values()),480);self.assertEqual(480-totals['W'],440)
        self.assertTrue(d['diary']['wasoExcludesTerminal']);self.assertEqual(d['diary']['expected']['tst'],390)
        self.assertNotEqual(d['architecture']['expected']['tst'],d['diary']['expected']['tst'])
    def test_week_rows_reconstruct_without_unknown_zero_fill(self):
        week=json.loads((C/'study/cases.json').read_text(encoding='utf-8'))['week'];rows=[r for r in week['rows'] if r is not None]
        self.assertEqual(len(rows),6);self.assertEqual(sum(r['tib'] for r in rows),2800);self.assertEqual(sum(r['tst'] for r in rows),2340)
        for r in rows:
            def minute(s):h,m=map(int,s.split(':'));return h*60+m
            bed=minute(r['bed']);end=minute(r['out'])+1440*r['dayOffset']
            self.assertEqual(end-bed,r['tib']);self.assertEqual(r['tib']-r['sol']-r['waso']-r['terminal'],r['tst'])
            mid=((bed+r['sol']+end-r['terminal'])/2)%1440;self.assertAlmostEqual(mid,r['mid'])
    def test_caffeine_denominators_and_wearable_cases(self):
        d=json.loads((C/'study/cases.json').read_text(encoding='utf-8'));c=d['caffeine'];self.assertAlmostEqual(c['initialMg']*2**(-c['hours']/c['halfLifeHours']),25)
        b=d['breathing'];self.assertEqual(b['events']/b['sleepHours'],6);self.assertEqual(b['events']/b['methodMonitoringHours'],4.5)
        w=d['wearable'];self.assertEqual(w['positive'],'sleep');self.assertEqual((w['tp']+w['fn'])*w['epochSeconds']/60,50);self.assertEqual((w['tp']+w['fp'])*w['epochSeconds']/60,65);self.assertIsNone(w['algorithmVersion'])
    def test_timezone_case_arithmetic_and_unknown_phase(self):
        z=json.loads((C/'study/cases.json').read_text(encoding='utf-8'))['timeZone'];self.assertIsNone(z['phaseMarker'])
        departure=datetime.fromisoformat(z['departureLocal']).replace(tzinfo=timezone(timedelta(minutes=z['fromOffsetMinutes'])))
        arrival=(departure+timedelta(minutes=z['elapsedMinutes'])).astimezone(timezone(timedelta(minutes=z['toOffsetMinutes'])))
        self.assertEqual(arrival.strftime('%Y-%m-%dT%H:%M'),z['expectedArrivalLocal'])
    def test_versions_and_source_limits_are_explicit(self):
        text=(C/'study/sources.md').read_text(encoding='utf-8')
        for term in ['2026-11-17','2026-10-24','2026-04-13','2025','2021','2022','2015','2016','查核日','授權','草案','Yellow Book']:self.assertIn(term,text)
        self.assertGreaterEqual(len(set(re.findall(r'https://[^)\s]+',text))),25)
    def test_resources_and_script_order(self):
        for rel in CAT['learningResources']:
            path=(C/rel).resolve();self.assertTrue(path.is_relative_to(C.resolve()) and path.is_file())
        page=(C/'index.html').read_text(encoding='utf-8');self.assertIn('../assets/health-visuals.css',page)
        self.assertLess(page.index('assets/course-data.js'),page.index('assets/overview.js'));self.assertLess(page.index('assets/overview.js'),page.index('../assets/reader.js'))

class SleepBundleTests(unittest.TestCase):
    def setUp(self):self.bundle=zipfile.ZipFile(C/CAT['studyBundle'])
    def tearDown(self):self.bundle.close()
    def test_complete_standalone_bundle(self):
        names=self.bundle.namelist();self.assertEqual(len(names),61);self.assertEqual(len(set(names)),61);self.assertEqual(sum(n.endswith('.svg') for n in names),54)
        self.assertTrue(all(n.startswith('study-pack/') and '..' not in PurePosixPath(n).parts for n in names));self.assertIsNone(self.bundle.testzip())
        self.assertTrue(all(not n.endswith(('.py','.exe','.dll')) for n in names))
    def test_archive_bytes_match_sources(self):
        for name in self.bundle.namelist():
            relative=PurePosixPath(name).relative_to('study-pack');self.assertEqual(self.bundle.read(name),(C/relative).read_bytes(),name)
    def test_markdown_links_resolve_without_website(self):
        names=set(self.bundle.namelist())
        for name in names:
            if not name.endswith('.md'):continue
            for link in re.findall(r'\]\(([^)]+)\)',self.bundle.read(name).decode('utf-8')):
                parsed=urlparse(link)
                if parsed.scheme or link.startswith('#'):continue
                self.assertIn(posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(parsed.path))),names,(name,link))
    def test_svg_members_parse(self):
        for name in self.bundle.namelist():
            if name.endswith('.svg'):self.assertEqual(ET.fromstring(self.bundle.read(name)).tag,SVG+'svg')
if __name__=='__main__':unittest.main()

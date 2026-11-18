"""Check first-aid versions, fixed learning cases, original diagrams and offline study integrity."""
import csv,io,json,re,posixpath,unittest,zipfile
from pathlib import Path,PurePosixPath
from urllib.parse import urlparse,unquote
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'first-aid'
CAT=json.loads((C/'course.json').read_text(encoding='utf-8'));SVG='{http://www.w3.org/2000/svg}'
def cases():return json.loads((C/'study/cases.json').read_text(encoding='utf-8'))
class FirstAidMaterialsTests(unittest.TestCase):
    def test_scope_metadata_and_chapter_boundaries(self):
        self.assertEqual((len(CAT['groups']),len(CAT['lessons']),len(CAT['visuals'])),(20,120,60))
        self.assertEqual(len({l['id'] for l in CAT['lessons']}),120)
        self.assertEqual([sum(l['group']==g['id'] for l in CAT['lessons']) for g in CAT['groups']],[6]*20)
        self.assertTrue(all(l['summary'] and isinstance(l['tags'],list) and l['tags'] for l in CAT['lessons']))
    def test_independent_core_and_advanced_scope(self):
        self.assertEqual(CAT['minimumDisplayEquations'],0)
        titles=' '.join(l['title'] for l in CAT['lessons']+CAT['groups'])
        for term in ['119','CPR','AED','嬰兒','哽塞','出血','止血帶','燒燙傷','中風','血糖','抽搐','過敏','中毒','一氧化碳','心理急救','災害','多人','實體']:
            self.assertIn(term,titles)
    def test_no_programming_requirement(self):
        self.assertNotIn('exampleBundle',CAT);self.assertFalse(any(l.get('example') for l in CAT['lessons']));self.assertFalse((C/'examples').exists())
    def test_all_lessons_have_relevant_figures(self):
        figs={f['id']:f for f in CAT['visuals']};self.assertEqual([sum(f['group']==g['id'] for f in figs.values()) for g in CAT['groups']],[3]*20)
        for l in CAT['lessons']:
            f=figs[l['visual']];self.assertEqual(f['group'],l['group']);self.assertIn(l['id'],f['lessons']);self.assertEqual(len(f['lessons']),2)
        self.assertEqual({l['visual'] for l in CAT['lessons']},set(figs))
    def test_distinct_substantive_lessons_and_tasks(self):
        tasks=[]
        for l in CAT['lessons']:
            text=(C/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
            self.assertGreater(len(re.findall(r'[\u4e00-\u9fff]',text)),650,l['id'])
            for term in ['## 核心概念與安全行動','## 放回急救情境','## 情境自我檢核','<details><summary>']:self.assertIn(term,text)
            self.assertIn(l['visualTask'],text);self.assertGreater(len(l['visualTask']),35);tasks.append(l['visualTask'])
        self.assertEqual(len(set(tasks)),120)
    def test_accessible_zoomable_images(self):
        for l in CAT['lessons']:
            text=(C/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
            self.assertEqual(text.count('<figure class="health-figure">'),1)
            self.assertIn('target="_blank" rel="noopener"',text)
            self.assertGreater(len(re.search(r'<img [^>]*alt="([^"]+)"',text)[1]),25)
    def test_safe_original_svg_structure(self):
        for f in CAT['visuals']:
            with self.subTest(figure=f['id']):
                root=ET.parse(C/f['file']).getroot();self.assertEqual(root.tag,SVG+'svg');self.assertEqual(root.attrib['role'],'img')
                self.assertTrue(root.find(SVG+'title').text);self.assertGreater(len(root.find(SVG+'desc').text),25)
                ids=[el.attrib['id'] for el in root.iter() if 'id' in el.attrib];self.assertEqual(len(ids),len(set(ids)))
                self.assertTrue(set(root.attrib['aria-labelledby'].split())<=set(ids))
                for el in root.iter():
                    self.assertNotIn(el.tag,[SVG+'script',SVG+'image',SVG+'foreignObject'])
                    self.assertFalse(any(k.lower().startswith('on') for k in el.attrib))
                    for k,v in el.attrib.items():
                        if k.endswith('href'):self.assertFalse(v.startswith(('http:','https:','//','data:')))
                for el in root.findall('.//'+SVG+'text'):
                    self.assertTrue(0<=float(el.attrib['x'])<=860);self.assertTrue(0<=float(el.attrib['y'])<=520)
    def test_manifest_sources_and_local_paths(self):
        self.assertEqual(json.loads((C/'assets/figures/manifest.json').read_text(encoding='utf-8')),CAT['visuals'])
        for f in CAT['visuals']:
            self.assertTrue((C/f['file']).resolve().is_relative_to(C.resolve()));self.assertGreater(len(f['note']),15)
            self.assertTrue(f['sources']);self.assertTrue(all(s['title'] and urlparse(s['url']).scheme=='https' and s.get('version') for s in f['sources']))
    def test_labels_do_not_share_identical_positions(self):
        for f in CAT['visuals']:
            root=ET.parse(C/f['file']).getroot();seen={}
            for t in root.findall('.//'+SVG+'text'):
                position=(float(t.attrib['x']),float(t.attrib['y']))
                self.assertNotIn(position,seen,(f['id'],t.text,seen.get(position)))
                seen[position]=t.text
    def test_complete_workbook_and_answers(self):
        for name in ['workbook.md','answers.md']:
            text=(C/'study'/name).read_text(encoding='utf-8');self.assertEqual(len(re.findall(r'^### 單元 ',text,re.M)),120)
            for l in CAT['lessons']:self.assertIn(l['title'],text)
        self.assertEqual((C/'study/workbook.md').read_text(encoding='utf-8').count('[看圖：'),120)
    def test_bilingual_glossary(self):
        data=(C/'study/glossary.csv').read_bytes();self.assertNotIn(b'\r\r\n',data)
        rows=list(csv.DictReader(io.StringIO(data.decode('utf-8-sig'))))
        self.assertEqual(len(rows),125);self.assertEqual(len({r['中文'] for r in rows}),125)
        self.assertTrue(all(r['English'] and len(r['學習用簡釋'])>15 for r in rows))
    def test_offline_scenario_script_matches_canonical_cases(self):
        text=(C/'assets/scenarios.js').read_text(encoding='utf-8')
        generated=json.loads(text.split('window.AID_SCENARIOS = ',1)[1].strip().removesuffix(';'))
        self.assertEqual(generated,cases());self.assertTrue(generated['synthetic']);self.assertEqual(generated['updated'],'2026-11-18')
    def test_fixed_scenarios_have_actions_reasons_and_real_lesson_targets(self):
        d=cases()
        for category in ['sceneSafety','recognition','aed','choking','bleeding','burns','myths']:
            values=d[category];self.assertEqual(len({x['key'] for x in values}),len(values))
            for x in values:
                self.assertGreater(len(x['scene']),10,x['key']);self.assertGreater(len(x['action']),20,x['key']);self.assertGreater(len(x['reason']),20,x['key'])
                self.assertTrue(1<=x['lesson']<=120)
        for category in ['callCard','strokeTimeline']:self.assertTrue(1<=d[category]['lesson']<=120)
    def test_lay_arrest_and_no_shock_actions_do_not_delay_cpr(self):
        d=cases();g=next(x for x in d['recognition'] if x['key']=='gasping');n=next(x for x in d['aed'] if x['key']=='no-shock')
        self.assertIn('119',g['action']);self.assertIn('CPR',g['action']);self.assertIn('不花時間摸脈',g['action'])
        self.assertIn('立即恢復CPR',n['action']);self.assertIn('不等於',n['reason'])
    def test_infant_choking_is_not_abdominal_thrusts(self):
        d=cases();i=next(x for x in d['choking'] if x['key']=='severe-infant');u=next(x for x in d['choking'] if x['key']=='unresponsive')
        self.assertIn('5次背部拍擊與5次胸部推壓',i['action']);self.assertIn('單掌根',i['action']);self.assertIn('不做腹部推壓',i['action'])
        self.assertIn('立即分工119',i['action'])
        self.assertIn('先胸外按壓',u['action']);self.assertIn('看得到',u['action']);self.assertIn('不盲目',u['reason'])
    def test_stroke_times_preserve_known_well_and_expose_delay(self):
        t=cases()['strokeTimeline'];self.assertEqual([x['time'] for x in t['events']],['08:00','08:40','08:50'])
        self.assertIn('08:40',t['action']);self.assertIn('立即119',t['action']);self.assertIn('延遲',t['action']);self.assertIn('不是建議等待',t['action'])
        self.assertIn('不由網頁判斷治療資格',t['reason'])
    def test_burn_timings_and_medical_limits_are_qualified(self):
        d=cases();b=next(x for x in d['burns'] if x['key']=='thermal');g=next(x for x in d['myths'] if x['key']=='glucose')
        self.assertIn('以約20分鐘為目標',b['action']);self.assertIn('119與保溫同步',b['action']);self.assertIn('至少10分鐘',b['reason']);self.assertIn('5–20分鐘',b['reason'])
        self.assertIn('不要經口',g['action']);self.assertIn('清醒且可安全吞嚥',g['reason'])
    def test_quiz_answers_and_preparedness_are_learning_not_certification(self):
        d=cases();self.assertEqual(len(d['quiz']),12);self.assertEqual(len(d['preparedness']),6)
        for q in d['quiz']:
            self.assertEqual(len(q['options']),3);self.assertIn(q['answer'],range(3));self.assertGreater(len(q['why']),15);self.assertTrue(1<=q['lesson']<=120)
        self.assertIn('實體模型',d['quiz'][5]['options'][d['quiz'][5]['answer']])
    def test_source_versions_population_and_training_boundaries(self):
        text=(C/'study/sources.md').read_text(encoding='utf-8')
        for term in ['2026-11-18','2025','2024','2026-02-06','2026-03-18','民眾','摸脈','地域','受訓','模型','15:2','30:2','20分鐘','不是建議等待']:self.assertIn(term,text)
        self.assertGreaterEqual(len(set(re.findall(r'https://[^)\s]+',text))),25)
    def test_learning_overview_has_no_patient_inputs_or_live_timers(self):
        text=(C/'assets/overview.js').read_text(encoding='utf-8')
        for pattern in [r'fetch\s*\(',r'XMLHttpRequest',r'navigator\.geolocation',r'setInterval\s*\(',r'performance\.now\s*\(']:self.assertNotRegex(text,pattern)
        self.assertNotIn('type="number"',text);self.assertNotIn('type="text"',text);self.assertNotIn('tel:',text)
    def test_local_resources_and_script_order(self):
        for rel in CAT['learningResources']:
            path=(C/rel).resolve();self.assertTrue(path.is_relative_to(C.resolve()) and path.is_file())
        page=(C/'index.html').read_text(encoding='utf-8');self.assertIn('../assets/health-visuals.css',page)
        self.assertLess(page.index('assets/course-data.js'),page.index('assets/scenarios.js'));self.assertLess(page.index('assets/scenarios.js'),page.index('assets/overview.js'));self.assertLess(page.index('assets/overview.js'),page.index('../assets/reader.js'))

class FirstAidBundleTests(unittest.TestCase):
    def setUp(self):self.bundle=zipfile.ZipFile(C/CAT['studyBundle'])
    def tearDown(self):self.bundle.close()
    def test_standalone_zip_scope_and_integrity(self):
        names=self.bundle.namelist();self.assertEqual(len(names),67);self.assertEqual(len(set(names)),67);self.assertEqual(sum(n.endswith('.svg') for n in names),60)
        self.assertTrue(all(n.startswith('study-pack/') and '..' not in PurePosixPath(n).parts for n in names));self.assertIsNone(self.bundle.testzip())
        self.assertFalse(any(n.endswith(('.py','.exe','.dll')) for n in names))
    def test_archive_matches_sources(self):
        for name in self.bundle.namelist():
            rel=PurePosixPath(name).relative_to('study-pack');self.assertEqual(self.bundle.read(name),(C/rel).read_bytes(),name)
    def test_markdown_links_resolve_inside_zip(self):
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

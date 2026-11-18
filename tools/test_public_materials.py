"""Check population definitions, original diagrams, provenance and offline study integrity."""
import csv,io,json,re,posixpath,unittest,zipfile
from pathlib import Path,PurePosixPath
from urllib.parse import urlparse,unquote
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'public-health'
CAT=json.loads((C/'course.json').read_text(encoding='utf-8'));SVG='{http://www.w3.org/2000/svg}'
def cases():return json.loads((C/'study/cases.json').read_text(encoding='utf-8'))
class PublicMaterialsTests(unittest.TestCase):
    def test_scope_metadata_and_chapter_boundaries(self):
        self.assertEqual((len(CAT['groups']),len(CAT['lessons']),len(CAT['visuals'])),(20,120,60))
        self.assertEqual(len({l['id'] for l in CAT['lessons']}),120)
        self.assertEqual([sum(l['group']==g['id'] for l in CAT['lessons']) for g in CAT['groups']],[6]*20)
        self.assertTrue(all(l['summary'] and isinstance(l['tags'],list) and l['tags'] for l in CAT['lessons']))
    def test_independent_core_and_advanced_scope(self):
        titles=' '.join(l['title'] for l in CAT['lessons'])
        for term in ['盛行率','人時','標準化','病例對照','勝算比','偏差','DAG','Simpson','不死時間','監測','SIR','聚餐','疫苗','抗藥性','篩檢','氣候','公平','UHC','ICER','IHR','PABS','倫理','溝通','專題']:
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
            for term in ['## 核心概念與方法','## 放回公共衛生情境','## 不寫程式的自我檢核','<details><summary>']:self.assertIn(term,text)
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
        self.assertEqual(len(rows),140);self.assertEqual(len({r['中文'] for r in rows}),140)
        self.assertTrue(all(r['English'] and len(r['學習用簡釋'])>15 for r in rows))
    def test_frequency_case_preserves_time_and_population(self):
        c=cases()['frequency'];e=c['expected'];atrisk=c['population']-c['existing']
        self.assertEqual(atrisk,900);self.assertEqual(atrisk,e['atRisk'])
        self.assertAlmostEqual(c['existing']/c['population'],e['prevalence']);self.assertAlmostEqual(c['newCases']/atrisk,e['risk'])
        self.assertAlmostEqual(c['newCases']/c['personYears'],e['ratePerPersonYear']);self.assertLessEqual(c['personYears'],atrisk*c['periodYears'])
        self.assertEqual(sum(r['people'] for r in c['personTimeComponents']),atrisk)
        self.assertAlmostEqual(sum(r['people']*r['atRiskYearsEach'] for r in c['personTimeComponents']),c['personYears'])
        self.assertNotIn('endPrevalence',c);self.assertNotAlmostEqual(e['risk'],e['ratePerPersonYear'])
    def test_cohort_and_outbreak_are_independent(self):
        for key in ['association','outbreakMeal']:
            c=cases()[key];a,b,x,d=[c[k] for k in ['a','b','c','d']];re=a/(a+b);ru=x/(x+d)
            self.assertAlmostEqual(re/ru,c['expected']['rr']);self.assertAlmostEqual(re-ru,c['expected']['rd']);self.assertAlmostEqual(a*d/(b*x),c['expected']['or'])
        self.assertNotEqual(cases()['association']['a'],cases()['outbreakMeal']['a'])
    def test_common_age_weights_reconstruct_standardized_rates(self):
        c=cases()['standardization'];self.assertAlmostEqual(sum(c['weights']),1)
        for group in ['a','b']:
            rows=c[group];self.assertAlmostEqual(sum(r['events'] for r in rows)/sum(r['n'] for r in rows),c['expected']['crude'+group.upper()])
            self.assertAlmostEqual(sum(w*r['events']/r['n'] for w,r in zip(c['weights'],rows)),c['expected']['adjusted'+group.upper()])
    def test_simpson_direction_and_outcome(self):
        c=cases()['simpson']
        for a,b in zip(c['e'],c['u']):self.assertLess(a['recovered']/a['n'],b['recovered']/b['n'])
        for group in ['e','u']:
            rows=c[group];self.assertAlmostEqual(sum(r['recovered'] for r in rows)/sum(r['n'] for r in rows),c['expected']['crude'+group.upper()])
            self.assertAlmostEqual(sum(w*r['recovered']/r['n'] for w,r in zip(c['weights'],rows)),c['expected']['adjusted'+group.upper()])
        self.assertGreater(c['expected']['crudeE'],c['expected']['crudeU']);self.assertLess(c['expected']['adjustedE'],c['expected']['adjustedU'])
    def test_line_list_unknown_onset_never_zero_filled(self):
        c=cases()['surveillance'];rows=c['lineList'];self.assertEqual(len(rows),34);self.assertEqual(len({r['id'] for r in rows}),34)
        self.assertEqual(sum(r['onsetDay'] is None for r in rows),3)
        self.assertEqual([sum(r['onsetDay']==day for r in rows) for day in range(1,11)],c['knownOnsetCounts'])
        self.assertTrue(all(r['onsetDay'] is None or r['reportDay']>=r['onsetDay'] for r in rows));self.assertEqual(sum(c['knownOnsetCounts']),31)
        p=cases()['completeness'];self.assertAlmostEqual(p['present']/p['expected'],p['fraction'])
    def test_vaccine_and_screen_expected_counts(self):
        c=cases()['vaccine'];self.assertAlmostEqual(1-(c['vCases']/c['vTotal'])/(c['uCases']/c['uTotal']),c['expected']['ve'])
        self.assertAlmostEqual(c['uCases']/c['uTotal']-c['vCases']/c['vTotal'],c['expected']['arr'])
        s=cases()['screening'];ppv=[]
        for x in s['scenarios']:
            self.assertAlmostEqual(x['tp'],s['n']*x['prevalence']*s['sensitivity']);self.assertAlmostEqual(x['fp'],s['n']*(1-x['prevalence'])*(1-s['specificity']))
            self.assertEqual(sum(x[k] for k in ['tp','fn','fp','tn']),s['n']);ppv.append(x['tp']/(x['tp']+x['fp']))
        self.assertLess(ppv[0],ppv[1])
    def test_equity_and_economic_scales(self):
        c=cases()['equity']
        for key in ['baseline','later']:
            r=c[key];self.assertAlmostEqual(r['worse']-r['better'],r['gap']);self.assertAlmostEqual(r['worse']/r['better'],r['ratio'])
        self.assertLess(c['later']['gap'],c['baseline']['gap']);self.assertGreater(c['later']['ratio'],c['baseline']['ratio'])
        e=cases()['economics'];self.assertAlmostEqual((e['costB']-e['costA'])/(e['effectB']-e['effectA']),e['expected']['icer'])
    def test_sir_case_specification_and_mass_conservation(self):
        c=cases()['sir'];self.assertEqual(c['s0']+c['i0']+c['r0'],c['population']);self.assertAlmostEqual(c['beta']/c['gamma'],c['expected']['basicReproduction'])
        s,i,r=c['s0'],c['i0'],c['r0'];dt=c['stepDays']
        for step in range(round(c['days']/dt)):
            infection=c['beta']*s*i/c['population']*dt;removal=c['gamma']*i*dt;s-=infection;i+=infection-removal;r+=removal
            self.assertTrue(s>=0 and i>=0 and r>=0);self.assertAlmostEqual(s+i+r,c['population'],places=8)
    def test_source_years_and_procedural_status_are_distinct(self):
        text=(C/'study/sources.md').read_text(encoding='utf-8')
        for term in ['2026-11-17','2026-11-13','2027','2026-06-19','2025-09-19','2024','GHE2023','World Health Statistics','資料年','查核日','採納','批准','生效','授權']:self.assertIn(term,text)
        self.assertGreaterEqual(len(set(re.findall(r'https://[^)\s]+',text))),30)
    def test_local_resources_and_script_order(self):
        for rel in CAT['learningResources']:
            path=(C/rel).resolve();self.assertTrue(path.is_relative_to(C.resolve()) and path.is_file())
        page=(C/'index.html').read_text(encoding='utf-8');self.assertIn('../assets/health-visuals.css',page)
        self.assertLess(page.index('assets/course-data.js'),page.index('assets/overview.js'));self.assertLess(page.index('assets/overview.js'),page.index('../assets/reader.js'))

class PublicBundleTests(unittest.TestCase):
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

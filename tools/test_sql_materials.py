"""Portable SQL teaching artifacts and source parity, independently of runtime SQL tests."""
import json,re,posixpath,unittest
from pathlib import Path,PurePosixPath
from zipfile import ZipFile
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];C=R/'sql'
class SQLMaterialsTests(unittest.TestCase):
    def test_complete_sources_and_contextual_diagrams(self):
        c=json.loads((C/'course.json').read_text(encoding='utf-8'))
        self.assertEqual((len(c['groups']),len(c['lessons']),len(c['visuals'])),(18,108,36))
        self.assertEqual(c['updated'],'2026-11-27');self.assertEqual(len({l['visualTask'] for l in c['lessons']}),108)
        for l in c['lessons']:
            s=(C/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
            self.assertGreater(len(s),1000);self.assertIn(l['visualTask'],s);self.assertNotIn('??',s)
    def test_complete_examples_archive_and_original_bytes(self):
        with ZipFile(C/'examples.zip') as z:
            self.assertIsNone(z.testzip());names=set(z.namelist())
            for f in ['fixtures.py','contracts.py','pipeline.py','dataharbor.py','orchestrator.py','workflow.py','warehouse.py','postgres_lab.py',
                      'README.md','DATA_DICTIONARY.md','RUNBOOK.md','VERIFICATION.md','test_examples.py','requirements-lock.txt','data/batch-001.json','data/batch-002.json','queries/08.sql']:
                self.assertIn('examples/'+f,names)
            self.assertEqual(len([n for n in names if re.fullmatch(r'examples/lab\d\d\.py',n)]),36)
            for n in names:
                self.assertNotIn('..',PurePosixPath(n).parts);self.assertNotIn('.runtime',PurePosixPath(n).parts)
                self.assertFalse(n.endswith(('.duckdb','.wal','.parquet')));self.assertEqual(z.read(n),(C/n).read_bytes())
    def test_portable_study_pack_with_accessible_figures(self):
        with ZipFile(C/'study-pack.zip') as z:
            self.assertIsNone(z.testzip());names=set(z.namelist());self.assertEqual(len([n for n in names if n.endswith('.svg')]),36)
            for f in ['worksheet.md','answers.md']:
                self.assertEqual(len(re.findall(r'^## ',z.read('study-pack/study/'+f).decode('utf-8'),re.M)),108)
            self.assertEqual(len(re.findall(r'^## ',z.read('study-pack/study/glossary.md').decode('utf-8'),re.M)),94)
            for n in names:
                if n.endswith('.svg'):
                    root=ET.fromstring(z.read(n));self.assertEqual(root.attrib['role'],'img');self.assertTrue(root.attrib['aria-labelledby'])
                    self.assertTrue(root.find('{http://www.w3.org/2000/svg}title').text);self.assertTrue(root.find('{http://www.w3.org/2000/svg}desc').text)
                self.assertEqual(z.read(n),(C/n.removeprefix('study-pack/')).read_bytes())
                if n.endswith('.md'):
                    for link in re.findall(r'\]\(([^)]+)\)',z.read(n).decode('utf-8')):
                        if '://' not in link and not link.startswith('#'):self.assertIn(posixpath.normpath(posixpath.join(posixpath.dirname(n),link)),names)
    def test_version_and_formula_contracts(self):
        v=json.loads((C/'study/versions.json').read_text(encoding='utf-8'));self.assertEqual(v['checked'],'2026-11-27')
        requirements=(C/'examples/requirements.txt').read_text(encoding='utf-8').lower()
        for k,version in v['packages'].items():self.assertIn(k+'=='+version,requirements)
        self.assertEqual(v['postgresql_server'],'19.0');self.assertEqual(v['postgresql_verification']['server_version'],190000)
        coverage=json.loads((R/'tools/math-topic-coverage.json').read_text(encoding='utf-8'))['courses']['sql']
        self.assertTrue(coverage['formulaSections'])
if __name__=='__main__':unittest.main()

import json,re,posixpath,unittest
from pathlib import Path,PurePosixPath
from zipfile import ZipFile
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];C=R/'django'
class DjangoMaterialsTests(unittest.TestCase):
    def test_catalog_and_sources(self):
        c=json.loads((C/'course.json').read_text(encoding='utf-8'))
        self.assertEqual((len(c['groups']),len(c['lessons']),len(c['visuals'])),(14,84,28))
        self.assertEqual(c['updated'],'2026-11-26')
        self.assertEqual(len({x['visualTask'] for x in c['lessons']}),84)
        for l in c['lessons']:
            s=(C/'chapters'/f'{l["id"]}.md').read_text(encoding='utf-8')
            self.assertGreater(len(s),1000);self.assertIn(l['visualTask'],s);self.assertNotIn('??',s)
    def test_complete_project_archive_and_source_bytes(self):
        with ZipFile(C/'examples.zip') as z:
            self.assertIsNone(z.testzip())
            for file in ['manage.py','requirements-lock.txt','README.md','VERIFICATION.md','desk/models.py',
                         'desk/migrations/0001_initial.py','desk/static/desk/app.css','desk/templates/desk/task_list.html',
                         'templates/registration/login.html','templates/registration/password_reset_confirm.html',
                         'desk/tests.py','studyhub/production.py']:
                self.assertIn('examples/'+file,z.namelist())
            self.assertEqual(len([n for n in z.namelist() if re.fullmatch(r'examples/\d\d_[^/]+\.py',n)]),24)
            for n in z.namelist():
                self.assertNotIn('..',PurePosixPath(n).parts)
                self.assertNotIn('staticfiles',PurePosixPath(n).parts);self.assertNotIn('private-media',PurePosixPath(n).parts)
                self.assertFalse(n.endswith('.sqlite3'));self.assertEqual(z.read(n),(C/n).read_bytes())
    def test_portable_study_pack_and_accessible_svg(self):
        with ZipFile(C/'study-pack.zip') as z:
            self.assertIsNone(z.testzip());names=set(z.namelist())
            self.assertEqual(len([n for n in names if n.endswith('.svg')]),28)
            for f in ['worksheet.md','answers.md']:
                s=z.read('study-pack/study/'+f).decode('utf-8');self.assertEqual(len(re.findall(r'^## ',s,re.M)),84)
            s=z.read('study-pack/study/glossary.md').decode('utf-8');self.assertEqual(len(re.findall(r'^## ',s,re.M)),104)
            for n in names:
                if n.endswith('.svg'):
                    root=ET.fromstring(z.read(n));self.assertEqual(root.attrib['role'],'img')
                    self.assertTrue(root.find('{http://www.w3.org/2000/svg}title').text)
                    self.assertTrue(root.find('{http://www.w3.org/2000/svg}desc').text)
                    self.assertEqual(z.read(n),(C/n.removeprefix('study-pack/')).read_bytes())
                if n.endswith('.md'):
                    for link in re.findall(r'\]\(([^)]+)\)',z.read(n).decode('utf-8')):
                        if '://' in link or link.startswith('#'):continue
                        self.assertIn(posixpath.normpath(posixpath.join(posixpath.dirname(n),link)),names)
    def test_version_pins_and_quantitative_topic_definitions(self):
        v=json.loads((C/'study/versions.json').read_text(encoding='utf-8'));self.assertEqual(v['checked'],'2026-11-26')
        requirements=(C/'examples/requirements.txt').read_text(encoding='utf-8').lower()
        for k,version in v['packages'].items():self.assertIn(k.lower()+'=='+version,requirements)
        coverage=json.loads((R/'tools/math-topic-coverage.json').read_text(encoding='utf-8'))['courses']['django']
        for lesson in ['011-middleware','027-related-loading','035-pagination','061-caching']:
            self.assertIn(lesson,coverage['formulaSections'])
if __name__=='__main__':unittest.main()

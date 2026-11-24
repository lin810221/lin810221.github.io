"""Verify editable-source correspondence and standalone Transformer downloads."""
import hashlib
import json
from pathlib import Path,PurePosixPath
import re
import unittest
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1];COURSE=ROOT/'transformer'

class TransformerMaterialsTests(unittest.TestCase):
    def test_catalog_source_and_tasks(self):
        c=json.loads((COURSE/'course.json').read_text(encoding='utf-8'))
        self.assertEqual((len(c['groups']),len(c['lessons']),len(c['visuals'])),(16,96,32))
        self.assertEqual(c['updated'],'2026-11-24')
        self.assertEqual({l['visual'] for l in c['lessons']},{f['id'] for f in c['visuals']})
        for lesson in c['lessons']:
            source=(COURSE/'chapters'/f"{lesson['id']}.md").read_text(encoding='utf-8')
            self.assertIn(lesson['visualTask'],source)

    def test_local_svg_accessibility(self):
        for path in (COURSE/'assets/figures').glob('*.svg'):
            text=path.read_text(encoding='utf-8');root=ET.fromstring(text)
            self.assertEqual(root.attrib.get('role'),'img')
            elements={e.attrib['id']:e for e in root.iter() if 'id' in e.attrib}
            for identifier in root.attrib['aria-labelledby'].split():self.assertTrue(''.join(elements[identifier].itertext()).strip())
            self.assertIsNotNone(root.find('{http://www.w3.org/2000/svg}title'))
            self.assertIsNotNone(root.find('{http://www.w3.org/2000/svg}desc'))
            self.assertNotRegex(text,r'<(?:script|foreignObject)\b|(?:href|src)=["\']https?://')

    def test_program_zip_current_and_complete(self):
        with ZipFile(COURSE/'examples.zip') as z:
            self.assertIsNone(z.testzip())
            for member in ['examples/lm_core.py','examples/requirements-lock.txt','examples/VERIFICATION.md','examples/test_examples.py']:
                self.assertIn(member,z.namelist())
            self.assertEqual(len([n for n in z.namelist() if re.fullmatch(r'examples/\d\d_[^/]+\.py',n)]),28)
            for name in z.namelist():
                self.assertNotIn('..',PurePosixPath(name).parts)
                path=COURSE/name;self.assertTrue(path.is_file())
                self.assertEqual(hashlib.sha256(z.read(name)).digest(),hashlib.sha256(path.read_bytes()).digest())

    def test_study_pack_portable_and_complete(self):
        with ZipFile(COURSE/'study-pack.zip') as z:
            self.assertIsNone(z.testzip());names=set(z.namelist())
            self.assertEqual(len([n for n in names if n.endswith('.svg')]),32)
            worksheet=z.read('study-pack/study/worksheet.md').decode('utf-8')
            self.assertEqual(len(re.findall(r'^## ',worksheet,re.M)),96)
            glossary=z.read('study-pack/study/glossary.md').decode('utf-8')
            self.assertIn('KV',glossary);self.assertIn('RoPE',glossary)
            for name in names:
                self.assertNotIn('..',PurePosixPath(name).parts)
                if not name.endswith('.md'):continue
                text=z.read(name).decode('utf-8')
                self.assertNotIn('根代理',text)
                for link in re.findall(r'\]\(([^)]+)\)',text):
                    if '://' in link or link.startswith('#'):continue
                    parts=[]
                    for part in (PurePosixPath(name).parent/PurePosixPath(link)).parts:
                        if part=='..':parts.pop()
                        elif part!='.':parts.append(part)
                    self.assertIn('/'.join(parts),names,(name,link))

    def test_version_baselines_match_requirements(self):
        data=json.loads((COURSE/'study/versions.json').read_text(encoding='utf-8'))
        self.assertEqual(data['checked'],'2026-11-24')
        requirements=(COURSE/'examples/requirements.txt').read_text(encoding='utf-8').lower()
        for name,version in data['packages'].items():self.assertIn(name.lower()+'=='+version,requirements)

if __name__=='__main__':unittest.main()

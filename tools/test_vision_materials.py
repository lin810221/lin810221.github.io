"""Check the downloadable artifacts and their original source correspondence."""
import hashlib
import json
from pathlib import Path,PurePosixPath
import re
import unittest
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
COURSE=ROOT/'image-recognition'


class VisionMaterialsTests(unittest.TestCase):
    def test_catalog_and_lesson_visuals(self):
        course=json.loads((COURSE/'course.json').read_text(encoding='utf-8'))
        self.assertEqual((len(course['groups']),len(course['lessons']),len(course['visuals'])),(14,84,28))
        self.assertEqual(course['updated'],'2026-11-23')
        self.assertEqual({l['visual'] for l in course['lessons']},{f['id'] for f in course['visuals']})
        for lesson in course['lessons']:
            text=(COURSE/'chapters'/f"{lesson['id']}.md").read_text(encoding='utf-8')
            self.assertIn(lesson['visualTask'],text)

    def test_original_local_svg_contract(self):
        for path in (COURSE/'assets/figures').glob('*.svg'):
            text=path.read_text(encoding='utf-8');root=ET.fromstring(text)
            self.assertEqual(root.attrib.get('role'),'img')
            self.assertIsNotNone(root.find('{http://www.w3.org/2000/svg}title'))
            self.assertIsNotNone(root.find('{http://www.w3.org/2000/svg}desc'))
            self.assertNotRegex(text,r'<(?:script|foreignObject)\b|(?:href|src)=["\']https?://')

    def test_program_bundle_is_current_and_complete(self):
        with ZipFile(COURSE/'examples.zip') as archive:
            self.assertIsNone(archive.testzip())
            self.assertIn('examples/vision_core.py',archive.namelist())
            self.assertIn('examples/requirements-lock.txt',archive.namelist())
            self.assertIn('examples/VERIFICATION.md',archive.namelist())
            scripts=[n for n in archive.namelist() if re.fullmatch(r'examples/\d\d_[^/]+\.py',n)]
            self.assertEqual(len(scripts),24)
            for name in archive.namelist():
                self.assertNotIn('..',PurePosixPath(name).parts)
                path=COURSE/name
                self.assertTrue(path.is_file())
                self.assertEqual(hashlib.sha256(archive.read(name)).digest(),hashlib.sha256(path.read_bytes()).digest())

    def test_study_bundle_links_are_portable(self):
        with ZipFile(COURSE/'study-pack.zip') as archive:
            self.assertIsNone(archive.testzip())
            names=set(archive.namelist())
            self.assertEqual(len([n for n in names if n.endswith('.svg')]),28)
            text=archive.read('study-pack/study/worksheet.md').decode('utf-8')
            self.assertEqual(len(re.findall(r'^## ',text,re.M)),84)
            for name in names:
                self.assertNotIn('..',PurePosixPath(name).parts)
                if not name.endswith('.md'):continue
                text=archive.read(name).decode('utf-8')
                self.assertNotIn('主代理',text)
                for link in re.findall(r'\]\(([^)]+)\)',text):
                    if '://' in link or link.startswith('#'):continue
                    parts=[]
                    for part in (PurePosixPath(name).parent/PurePosixPath(link)).parts:
                        if part=='..':parts.pop()
                        elif part!='.':parts.append(part)
                    self.assertIn('/'.join(parts),names,(name,link))


if __name__=='__main__':unittest.main()

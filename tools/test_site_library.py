"""Homepage publishing contracts: complete catalog, safe output and reproducibility."""
import copy
import json
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from build_library import ROOT, library_data, outputs
from validate import InspectHTML


class LibraryTests(unittest.TestCase):
    def test_all_courses_are_organized_once(self):
        data = library_data()
        self.assertEqual({c['slug'] for c in data['courses']}, {p.parent.name for p in ROOT.glob('*/course.json')})
        self.assertEqual(len(data['courses']), len({c['slug'] for c in data['courses']}))
        for c in data['courses']:
            original = json.loads((ROOT/c['slug']/'course.json').read_text(encoding='utf-8'))
            self.assertEqual(c['units'], [l['id'] for l in original['lessons']])
            self.assertEqual(c['updated'], original['updated'])

    def test_generated_artifacts_are_current(self):
        for relative, content in outputs().items():
            self.assertEqual((ROOT/relative).read_text(encoding='utf-8'), content, relative)

    def test_preserved_course_icons_are_local_vector_assets(self):
        for course in library_data()['courses']:
            icon = ROOT/'assets/course-icons'/f'{course["slug"]}.svg'
            root = ET.fromstring(icon.read_text(encoding='utf-8'))
            self.assertEqual(root.attrib['viewBox'], '0 0 260 180')
            self.assertGreater(len(list(root)), 0)
            for node in root.iter():
                self.assertNotEqual(node.tag.rsplit('}', 1)[-1], 'script')
                self.assertNotIn('href', node.attrib)

    def test_missing_metadata_fails_instead_of_hiding_a_course(self):
        data = json.loads((ROOT/'tools/library.json').read_text(encoding='utf-8'))
        data['courses'].pop('django')
        with patch('build_library.json.loads', return_value=data):
            with self.assertRaisesRegex(ValueError, 'Every course needs library metadata'):
                library_data()

    def test_escaped_editorial_text_and_local_assets(self):
        data = copy.deepcopy(library_data())
        data['courses'][0]['description'] = '<script>alert("x")</script> & test'
        data['courses'][0]['classic']['description'] = '<script>alert("x")</script> & test'
        with patch('build_library.library_data', return_value=data):
            page = outputs()['index.html']
        self.assertIn('&lt;script&gt;', page)
        self.assertNotIn('<script>alert', page)
        parsed = InspectHTML(); parsed.feed(page)
        for link in parsed.links:
            if link.startswith('#'): continue
            self.assertNotIn('://', link, 'Homepage must work offline')
            self.assertTrue((ROOT/link.split('#')[0]).is_file(), link)


if __name__ == '__main__':
    unittest.main()

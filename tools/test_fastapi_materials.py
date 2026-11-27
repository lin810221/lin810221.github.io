"""Portable project and source contracts, independent of installed ASGI runtime."""
import ast
import json
import posixpath
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / 'fastapi'


class FastAPIMaterialsTests(unittest.TestCase):
    def test_original_units_and_mechanism_coverage(self):
        course = json.loads((COURSE / 'course.json').read_text(encoding='utf-8'))
        self.assertEqual((len(course['groups']), len(course['lessons']), len(course['visuals'])), (16, 96, 32))
        self.assertEqual(len({lesson['visualTask'] for lesson in course['lessons']}), 96)
        self.assertEqual({lesson['visual'] for lesson in course['lessons']}, {f['id'] for f in course['visuals']})
        for lesson in course['lessons']:
            source = (COURSE / 'chapters' / (lesson['id'] + '.md')).read_text(encoding='utf-8')
            self.assertGreater(len(source), 1200)
            self.assertIn(lesson['visualTask'], source)
            self.assertNotIn('???', source)

    def test_full_project_archive_includes_deployment_and_client_sources(self):
        with ZipFile(COURSE / 'examples.zip') as archive:
            self.assertIsNone(archive.testzip())
            names = set(archive.namelist())
            for file in ['app.py', 'manage.py', 'gateway/api.py', 'gateway/store.py', 'gateway/providers.py', 'gateway/contracts.py', 'gateway/worker.py', 'gateway/security.py', 'migrations/env.py', 'migrations/versions/0001_initial.py', 'client.html', 'client.js', 'sse-client.js', 'Dockerfile', '.dockerignore', 'compose.yaml', 'socket_smoke.py', 'test_examples.py', 'requirements-lock.txt', 'README.md', 'RUNBOOK.md', 'VERIFICATION.md', 'DATA_DICTIONARY.md']:
                self.assertIn('examples/' + file, names)
            self.assertEqual(len([n for n in names if re.fullmatch(r'examples/lab\d\d\.py', n)]), 32)
            for name in names:
                self.assertNotIn('..', PurePosixPath(name).parts)
                self.assertNotIn('.runtime', PurePosixPath(name).parts)
                self.assertNotIn('.venv', PurePosixPath(name).parts)
                self.assertFalse(name.endswith(('.sqlite3', '.env')))
                self.assertEqual(archive.read(name), (COURSE / name).read_bytes())
                if name.endswith('.py'):
                    ast.parse(archive.read(name).decode('utf-8'))

    def test_study_bundle_links_accessibility_and_source_parity(self):
        with ZipFile(COURSE / 'study-pack.zip') as archive:
            self.assertIsNone(archive.testzip())
            names = set(archive.namelist())
            self.assertEqual(len([n for n in names if n.endswith('.svg')]), 32)
            for filename in ['worksheet.md', 'answers.md']:
                self.assertEqual(len(re.findall(r'^## ', archive.read('study-pack/study/' + filename).decode('utf-8'), re.M)), 96)
            self.assertEqual(len(re.findall(r'^## ', archive.read('study-pack/study/glossary.md').decode('utf-8'), re.M)), 107)
            for name in names:
                self.assertEqual(archive.read(name), (COURSE / name.removeprefix('study-pack/')).read_bytes())
                if name.endswith('.svg'):
                    root = ET.fromstring(archive.read(name))
                    self.assertEqual(root.attrib['role'], 'img')
                    self.assertTrue(root.attrib['aria-labelledby'])
                    self.assertTrue(root.find('{http://www.w3.org/2000/svg}title').text)
                    self.assertTrue(root.find('{http://www.w3.org/2000/svg}desc').text)
                if name.endswith('.md'):
                    for link in re.findall(r'\]\(([^)]+)\)', archive.read(name).decode('utf-8')):
                        if '://' not in link and not link.startswith('#'):
                            self.assertIn(posixpath.normpath(posixpath.join(posixpath.dirname(name), link)), names)

    def test_versions_and_quantitative_definitions(self):
        versions = json.loads((COURSE / 'study/versions.json').read_text(encoding='utf-8'))
        self.assertEqual(versions['python'], '3.15.2')
        self.assertEqual(versions['checked'], '2026-11-27')
        self.assertEqual(versions['core_tests'], 52)
        self.assertEqual(len(versions['packages']), 31)
        lock = (COURSE / 'examples/requirements-lock.txt').read_text(encoding='utf-8').lower()
        for name, version in versions['packages'].items():
            self.assertIn(name.lower() + '==' + version, lock)
        sections = json.loads((ROOT / 'tools/math-topic-coverage.json').read_text(encoding='utf-8'))['courses']['fastapi']['formulaSections']
        for identifier in ['022-deadlines', '024-bounded-retries', '029-idempotency-identity', '052-lease-fencing', '056-sse-replay', '062-token-bucket', '063-little-capacity', '065-health-slo', '088-horizontal-scaling', '092-formula-reference']:
            self.assertIn(identifier, sections)


if __name__ == '__main__':
    unittest.main()

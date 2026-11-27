"""Compile editable Markdown into file:// compatible course data; no server required."""
import html
import argparse
import json
import re
import zipfile
import shutil
import subprocess
from pathlib import Path
import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.preprocessors import Preprocessor
import xml.etree.ElementTree as ET
from pygments.formatters import HtmlFormatter
from audit_math_prose import assert_math_prose

ROOT = Path(__file__).resolve().parents[1]

def build_study_bundle(course_path, catalog):
    """Package non-code learning materials without requiring an examples folder."""
    bundle = catalog.get("studyBundle")
    if not bundle:
        return
    if not re.fullmatch(r"[a-zA-Z0-9_-]+\.zip", bundle):
        raise ValueError("Study bundle must be a ZIP filename")
    selected = set()
    for item in catalog.get("studyFiles", []):
        source = (course_path / item).resolve()
        if not source.is_relative_to(course_path.resolve()) or not source.exists():
            raise ValueError(f"Invalid study resource: {item}")
        for path in ([source] if source.is_file() else source.rglob("*")):
            if path.is_file() and path.suffix in {".md", ".csv", ".json", ".svg", ".txt"}:
                if not path.resolve().is_relative_to(course_path.resolve()):
                    raise ValueError("Study resource escapes its course")
                if not any(part.startswith(".") for part in path.relative_to(course_path.resolve()).parts):
                    selected.add(path)
    if not selected:
        raise ValueError("Study bundle cannot be empty")
    with zipfile.ZipFile(course_path / bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(selected):
            relative = path.relative_to(course_path.resolve())
            info = zipfile.ZipInfo("study-pack/" + relative.as_posix(), date_time=(2026, 11, 16, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())

def assert_readable(text, label):
    """UTF-8 can faithfully contain already-lost ASCII question marks."""
    prose = re.sub(r"(`{3,}|~{3,})[^\n]*\n.*?\1[^\n]*", "", text, flags=re.S)
    prose = re.sub(r"`[^`\n]*`", "", prose)
    if re.search(r"\?{3,}|\ufffd", prose):
        raise ValueError(f"Damaged text in {label}: replacement characters/question-mark runs")
    if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',text):
        raise ValueError(f'Invisible control character in {label}')


def math_markup(tex, display=False):
    tag = "div" if display else "span"
    cls = "math-block" if display else "math-source"
    delimiter = "$$" if display else "$"
    return f'<{tag} class="{cls}" data-tex="{html.escape(tex, quote=True)}" data-display="{str(display).lower()}">{delimiter}{html.escape(tex)}{delimiter}</{tag}><!--math-end-->'


def summary_math(summary):
    pattern = re.compile(r'(?<![\\$])\$(?!\$)([^\n$]+?)\$(?!\$)|\\\((.*?)\\\)')
    parts=[];start=0
    for match in pattern.finditer(summary):
        parts.append(html.escape(summary[start:match.start()]))
        parts.append(math_markup(next(v for v in match.groups() if v is not None)))
        start=match.end()
    parts.append(html.escape(summary[start:]));return ''.join(parts)


class ProtectedMath(Preprocessor):
    """Stash TeX BEFORE tables/escaping; leave fenced and inline code intact."""
    def markup(self, tex, display):
        return math_markup(tex,display)

    def run(self, lines):
        text = "\n".join(lines)
        # Fences have priority over math, including code examples containing $$.
        pieces = re.split(r"((?:^`{3,}[^\n]*\n.*?^`{3,}[^\n]*$)|(?:^~{3,}[^\n]*\n.*?^~{3,}[^\n]*$))", text, flags=re.M|re.S)
        pattern = re.compile(r"(?P<code>`+)(?P<codebody>[^\n]*?)(?P=code)|(?<!\\)\$\$(?P<dollarblock>.*?)\$\$|\\\[(?P<bracketblock>.*?)\\\]|\\\((?P<paren>.*?)\\\)|(?<![\\$])\$(?!\$)(?P<inline>[^\n$]+?)(?<!\\)\$(?!\$)", re.S)
        def replace(match):
            if match.group('code') is not None:return match.group()
            display = match.group('dollarblock') is not None or match.group('bracketblock') is not None
            tex = next(v for v in [match.group('dollarblock'),match.group('bracketblock'),match.group('paren'),match.group('inline')] if v is not None).strip()
            stored = self.md.htmlStash.store(self.markup(tex,display))
            return '\n\n'+stored+'\n\n' if display else stored
        for i in range(0,len(pieces),2):
            pieces[i]=pattern.sub(replace,pieces[i])
            if re.search(r"(?<!\\)\$\$|\\\[",re.sub(r'`+[^\n]*?`+','',pieces[i])):
                raise ValueError('Unclosed display math delimiter')
        return ''.join(pieces).split('\n')

class MathExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(ProtectedMath(md), "protected_math", 27)

def build(course_path):
    catalog = json.loads((course_path / "course.json").read_text(encoding="utf-8"))
    count = 0
    for lesson in catalog["lessons"]:
        source = (course_path / "chapters" / (lesson["id"] + ".md")).read_text(encoding="utf-8")
        assert_readable(lesson['title']+'\n'+lesson['summary'], lesson['id']+' metadata')
        assert_readable(source, lesson['id'])
        assert_math_prose(source,course_path.name+'/'+lesson['id'])
        assert_math_prose(lesson['summary'],course_path.name+'/'+lesson['id']+'/summary')
        source = re.sub(r"<!-- example:([a-zA-Z0-9_]+\.py) -->", lambda m: "```python\n" + (course_path / "examples" / m.group(1)).read_text(encoding="utf-8").rstrip() + "\n```", source)
        md = markdown.Markdown(extensions=["fenced_code", "tables", "toc", "attr_list", "codehilite", MathExtension()], extension_configs={"codehilite": {"guess_lang": False}, "toc": {"permalink": False}})
        lesson["html"] = md.convert(source)
        lesson['summaryHTML'] = summary_math(lesson['summary'])
        languages = iter(re.findall(r"^```([^\s`]*)", source, re.M)[::2])
        lesson["html"] = re.sub(r'<div class="codehilite">', lambda _: '<div class="codehilite" data-language="' + html.escape(next(languages, "code"), quote=True) + '">', lesson["html"])
        lesson["text"] = source
        lesson["toc"] = md.toc_tokens
        lesson["minutes"] = max(4, round(len(re.findall(r"[\u4e00-\u9fff]", source)) / 210 + len(re.findall(r"^", source, re.M)) / 22))
        count += len(source)
    (course_path / "assets").mkdir(parents=True, exist_ok=True)
    (course_path / "assets" / "course-data.js").write_text("/* Generated by tools/build.py. Edit chapters/*.md and course.json. */\nwindow.COURSE = " + json.dumps(catalog, ensure_ascii=False) + ";\n", encoding="utf-8")
    if catalog.get("exampleBundle"):
        bundle = catalog["exampleBundle"]
        if not re.fullmatch(r"[a-zA-Z0-9_-]+\.zip", bundle):
            raise ValueError("Example bundle must be a ZIP filename")
        examples = course_path / "examples"
        with zipfile.ZipFile(course_path / bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            excluded_directories = set(catalog.get('exampleExcludeDirectories', []))
            for example_path in sorted(examples.rglob("*")):
                relative = example_path.relative_to(examples)
                if any(part.startswith(".") or part == "__pycache__" or part in excluded_directories for part in relative.parts):
                    continue
                allowed_extensions = {".py", ".md", ".txt", ".json", ".sql", ".csv"} | set(catalog.get('exampleFileExtensions', []))
                if example_path.is_file() and example_path.suffix in allowed_extensions:
                    info = zipfile.ZipInfo("examples/" + relative.as_posix(), date_time=(2026, 10, 29, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, example_path.read_bytes())
    build_study_bundle(course_path, catalog)
    style = HtmlFormatter(style="github-dark").get_style_defs(".codehilite")
    (ROOT / "assets" / "syntax.css").write_text(style, encoding="utf-8")
    print(f"Built {course_path.name}: {len(catalog['lessons'])} units / {count:,} source characters")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("subjects", nargs="*", help="Subject folders; default: all courses")
    parser.add_argument('--require-prerender',action='store_true',help='Fail if Node is unavailable for static KaTeX rendering')
    args = parser.parse_args()
    names = args.subjects or [p.parent.name for p in sorted(ROOT.glob("*/course.json"))]
    for name in names:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
            parser.error(f"Invalid subject folder: {name}")
        build(ROOT / name)
    from build_library import build_library
    build_library()
    if shutil.which('node'):
        subprocess.run(['node',str(ROOT/'tools/render_math_cli.mjs'),*names],check=True,cwd=ROOT)
    elif args.require_prerender:
        raise RuntimeError('Node is required for publishable, pre-rendered mathematics')

"""Check generated course, local links, editable sources, code and offline fonts."""
import ast
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
LEGACY_TITLE_NUMBER = re.compile(r"^(?:\d+(?:-\d+)+|(?:習題|附錄)\s*[0-9A-Za-z]+)[\s\u3000]")


class InspectHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.headings = []
        self.math = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag in ("h2", "h3"):
            self.headings.append(attrs.get("id"))
        if "math-block" in attrs.get("class", "").split():
            self.math += 1


def local_links_exist(links, base):
    count = 0
    for link in links:
        parsed = urlparse(link)
        if parsed.scheme or link.startswith(("#", "//")):
            continue
        path = (base / unquote(parsed.path)).resolve()
        assert path.is_relative_to(ROOT), f"Out-of-workspace link: {link}"
        assert path.is_file(), f"Missing local file: {path}"
        count += 1
    return count


def walk_toc(items):
    for item in items:
        yield item
        yield from walk_toc(item.get("children", []))


def validate_course(course_path):
    data_path = course_path / "assets" / "course-data.js"
    raw = data_path.read_text(encoding="utf-8")
    course = json.loads(raw.split("window.COURSE = ", 1)[1].rstrip().removesuffix(";"))
    expected = json.loads((course_path / "course.json").read_text(encoding="utf-8"))
    assert len(course["lessons"]) == len(expected["lessons"])
    assert len({lesson["id"] for lesson in course["lessons"]}) == len(course["lessons"])
    source_ids = {path.stem for path in (course_path / "chapters").glob("*.md")}
    expected_ids = {lesson["id"] for lesson in expected["lessons"]}
    assert source_ids == expected_ids, f"Chapter sources/catalog mismatch in {course_path.name}: {sorted(source_ids ^ expected_ids)}"
    group_ids = {group["id"] for group in course["groups"]}
    assert len(group_ids) == len(course["groups"]), f"Duplicate chapter IDs: {course_path.name}"
    chapter_numbers = [int(group["number"]) for group in course["groups"] if group["number"].isdigit()]
    assert chapter_numbers == list(range(1, len(chapter_numbers) + 1)), f"Chapters must be numbered in order: {course_path.name}"
    for group in course["groups"]:
        assert any(lesson["group"] == group["id"] for lesson in course["lessons"]), f"Empty chapter: {group['id']}"
    visuals = {figure["id"]: figure for figure in course.get("visuals", [])}
    if visuals:
        assert len(visuals) == len(course["visuals"]), "Duplicate figure catalog IDs"
        for figure in visuals.values():
            path = (course_path / figure["file"]).resolve()
            assert path.is_relative_to(course_path.resolve()) and path.is_file()
            svg = ET.fromstring(path.read_text(encoding="utf-8"))
            assert svg.attrib.get("role") == "img"
            elements = {el.attrib["id"]: el for el in svg.iter() if "id" in el.attrib}
            for identifier in svg.attrib.get("aria-labelledby", "").split():
                assert identifier in elements and "".join(elements[identifier].itertext()).strip()
            assert svg.find("{http://www.w3.org/2000/svg}title") is not None
            assert svg.find("{http://www.w3.org/2000/svg}desc") is not None
    link_count = math_count = code_count = 0
    for page in (ROOT / "index.html", course_path / "index.html"):
        parsed = InspectHTML()
        parsed.feed(page.read_text(encoding="utf-8"))
        assert len(parsed.ids) == len(set(parsed.ids)), f"Duplicate IDs in {page}"
        link_count += local_links_exist(parsed.links, page.parent)
    for lesson in course["lessons"]:
        assert lesson["group"] in group_ids
        assert isinstance(lesson.get("summary"), str) and lesson["summary"].strip(), f"Missing lesson summary: {lesson['id']}"
        assert isinstance(lesson.get("tags"), list) and all(isinstance(tag, str) and tag.strip() for tag in lesson["tags"]), f"Invalid lesson tags: {lesson['id']}"
        assert not LEGACY_TITLE_NUMBER.match(lesson["title"]), f"Remove manual section numbering from title: {lesson['id']}"
        assert lesson["title"] == next(item["title"] for item in expected["lessons"] if item["id"] == lesson["id"]), f"Rebuild changed title: {lesson['id']}"
        assert len(lesson["text"]) > 1000, f"Missing substantial content: {lesson['id']}"
        if visuals:
            assert lesson.get("visual") in visuals, f"Missing lesson figure: {lesson['id']}"
            assert visuals[lesson["visual"]]["file"] in lesson["html"]
        assert "<!-- example:" not in lesson["text"]
        assert lesson["text"].count("```") % 2 == 0
        parsed = InspectHTML()
        parsed.feed(lesson["html"])
        assert len(parsed.ids) == len(set(parsed.ids)), f"Duplicate heading IDs: {lesson['id']}"
        assert len(parsed.headings) >= 4, f"Not enough sections: {lesson['id']}"
        for entry in walk_toc(lesson["toc"]):
            assert entry["id"] in parsed.ids, f"Broken TOC: {lesson['id']}"
        link_count += local_links_exist(parsed.links, course_path)
        math_count += parsed.math
        assert "https://" in lesson["html"], f"Missing sources: {lesson['id']}"
        if lesson.get("example"):
            example = course_path / "examples" / lesson["example"]
            ast.parse(example.read_text(encoding="utf-8"))
            code_count += 1
    css = (ROOT / "assets" / "vendor" / "katex" / "katex.min.css").read_text(encoding="utf-8")
    font_urls = re.findall(r"url\(([^)]+)\)", css)
    for url in font_urls:
        assert (ROOT / "assets" / "vendor" / "katex" / url.strip('"\'')).is_file(), f"Missing offline font: {url}"
    minimum_math = course.get("minimumDisplayEquations", 6 if course_path.name == "langgraph" else 4)
    assert type(minimum_math) is int and minimum_math >= 0, "Invalid display equation requirement"
    assert math_count >= minimum_math
    print(f"PASS {course_path.name}: {len(course['lessons'])} units, {code_count} linked examples, {link_count} local links, {len(font_urls)} offline fonts, {math_count} display equations")


def main():
    for catalog in sorted(ROOT.glob("*/course.json")):
        validate_course(catalog.parent)


if __name__ == "__main__":
    main()

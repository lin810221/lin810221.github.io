"""Check generated course, local links, editable sources, code and offline fonts."""
import ast
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]


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
    group_ids = {group["id"] for group in course["groups"]}
    link_count = math_count = code_count = 0
    for page in (ROOT / "index.html", course_path / "index.html"):
        parsed = InspectHTML()
        parsed.feed(page.read_text(encoding="utf-8"))
        assert len(parsed.ids) == len(set(parsed.ids)), f"Duplicate IDs in {page}"
        link_count += local_links_exist(parsed.links, page.parent)
    for lesson in course["lessons"]:
        assert lesson["group"] in group_ids
        assert len(lesson["text"]) > 1000, f"Missing substantial content: {lesson['id']}"
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
    assert math_count >= (6 if course_path.name == "langgraph" else 4)
    print(f"PASS {course_path.name}: {len(course['lessons'])} chapters, {code_count} linked examples, {link_count} local links, {len(font_urls)} offline fonts, {math_count} display equations")


def main():
    for catalog in sorted(ROOT.glob("*/course.json")):
        validate_course(catalog.parent)


if __name__ == "__main__":
    main()

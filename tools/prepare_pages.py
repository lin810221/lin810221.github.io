"""Prepare runtime website files for browser upload or automated GitHub Pages deployment."""
import argparse
import json
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlparse
from validate import InspectHTML

ROOT = Path(__file__).resolve().parents[1]
ASSET_SUFFIXES = {".js", ".css", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".woff2", ".txt"}


def check_links(links, base, destination):
    for link in links:
        parsed = urlparse(link)
        if parsed.scheme or link.startswith(("#", "//")):
            continue
        target = (base / unquote(parsed.path)).resolve()
        if not target.is_relative_to(destination) or not target.is_file():
            raise ValueError(f"Missing published file: {link}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("browser", "pages"), default="browser")
    args = parser.parse_args()
    destination = (ROOT / ("github-upload" if args.target == "browser" else "dist")).resolve()
    assert destination.parent == ROOT, "Output must stay in this workspace"
    selected = {Path("index.html"), Path(".nojekyll")}
    courses = []
    for path in (ROOT / "assets").rglob("*"):
        if path.is_file() and path.suffix.lower() in ASSET_SUFFIXES:
            selected.add(path.relative_to(ROOT))
    for catalog in sorted(ROOT.glob("*/course.json")):
        folder = catalog.parent
        course = json.loads((folder / "assets" / "course-data.js").read_text(encoding="utf-8").split("window.COURSE = ", 1)[1].rstrip().removesuffix(";"))
        courses.append((folder.name, course))
        selected.add(Path(folder.name) / "index.html")
        for path in (folder / "assets").rglob("*"):
            if path.is_file() and path.suffix.lower() in ASSET_SUFFIXES:
                selected.add(path.relative_to(ROOT))
        selected.add(Path(folder.name) / "examples" / "README.md")
        if course.get("exampleBundle"):
            selected.add(Path(folder.name) / course["exampleBundle"])
        else:
            for lesson in course["lessons"]:
                if lesson.get("example"):
                    selected.add(Path(folder.name) / "examples" / lesson["example"])
            for name in ("requirements.txt", "test_examples.py"):
                path = folder / "examples" / name
                if path.is_file():
                    selected.add(path.relative_to(ROOT))
    allowed = selected | {Path("README.md")}
    if destination.exists():
        unexpected = {path.relative_to(destination) for path in destination.rglob("*") if path.is_file()} - allowed
        if unexpected:
            raise ValueError("Upload folder contains unrelated or stale files; inspect it before refreshing")
    for relative in sorted(selected):
        source = ROOT / relative
        if not source.is_file():
            raise FileNotFoundError(f"Build the website first: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    readme = "# Learning Notes\n\n" + "\n".join(
        f"- [{course['title']}]({folder}/index.html): {len(course['lessons'])} chapters"
        for folder, course in courses
    ) + "\n\nThis repository contains the published static website and downloadable examples.\n"
    (destination / "README.md").write_text(readme, encoding="utf-8")
    for relative in selected:
        if relative.suffix == ".html":
            parser = InspectHTML()
            parser.feed((destination / relative).read_text(encoding="utf-8"))
            check_links(parser.links, (destination / relative).parent, destination)
    for folder, course in courses:
        for lesson in course["lessons"]:
            parser = InspectHTML()
            parser.feed(lesson["html"])
            check_links(parser.links, destination / folder, destination)
    for css in destination.rglob("*.css"):
        for url in re.findall(r"url\(([^)]+)\)", css.read_text(encoding="utf-8")):
            check_links([url.strip('"\'')], css.parent, destination)
    files = [path for path in destination.rglob("*") if path.is_file()]
    if args.target == "browser" and (destination / ".nojekyll").stat().st_size == 0:
        raise ValueError("Use a nonempty .nojekyll so browser uploads can include it")
    if args.target == "browser" and (len(files) > 100 or any(path.stat().st_size > 25 * 1024 * 1024 for path in files)):
        raise ValueError("Package exceeds GitHub browser upload limits")
    print(f"PASS {args.target}: {len(files)} files, {sum(path.stat().st_size for path in files):,} bytes; all local links and fonts verified")
    if args.target == "browser":
        print("Upload the CONTENTS of github-upload, not the github-upload folder itself.")
    else:
        print("GitHub Pages artifact directory: dist")


if __name__ == "__main__":
    main()

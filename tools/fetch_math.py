"""Download pinned KaTeX distribution from npm; only writes the workspace vendor folder."""
import io
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets" / "vendor" / "katex"
URL = "https://registry.npmjs.org/katex/-/katex-0.16.22.tgz"

def main():
    data = urllib.request.urlopen(URL, timeout=45).read()
    count = 0
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for member in archive.getmembers():
            prefix = "package/dist/"
            if not member.isfile() or not member.name.startswith(prefix):
                continue
            relative = Path(member.name[len(prefix):])
            if relative.name not in {"katex.min.js", "katex.min.css", "auto-render.min.js"} and relative.suffix != ".woff2":
                continue
            target = (DEST / relative).resolve()
            if not target.is_relative_to(DEST.resolve()):
                raise ValueError("Invalid archive path")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
            count += 1
        license_file = archive.extractfile("package/LICENSE")
        (DEST / "LICENSE.txt").write_bytes(license_file.read())
    # The browser uses woff2; remove fallback URLs to unshipped font formats.
    css_path = DEST / "katex.min.css"
    import re
    css = css_path.read_text(encoding="utf-8")
    css = re.sub(r',url\([^)]*\) format\("(?:woff|truetype)"\)', '', css)
    css_path.write_text(css, encoding="utf-8")
    print(f"KaTeX 0.16.22: {count} assets downloaded")

if __name__ == "__main__":
    main()

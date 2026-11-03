"""Read only a bounded .txt file inside a temporary allowlisted directory."""
from pathlib import Path
from tempfile import TemporaryDirectory
from integration_core import safe_file


if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        root = Path(folder) / "documents"
        root.mkdir()
        (root / "guide.txt").write_text("MCP course fixture", encoding="utf-8")
        (Path(folder) / "outside.txt").write_text("not shared", encoding="utf-8")
        print(safe_file(root, "guide.txt"))
        try:
            safe_file(root, "../outside.txt")
        except PermissionError:
            print("path traversal rejected")
    print("This example assumes the directory cannot be modified by an attacker during open().")

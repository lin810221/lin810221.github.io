"""Inspect term positions, not merely a list of matching documents."""
import json
from search_core import postings

if __name__ == "__main__":
    index = postings({"a":"usb hub usb","b":"usb cable","c":"cable hub"})
    print(json.dumps(index,indent=2))
    assert index["usb"]["a"] == [0,2]
    print("Phrase evaluation needs adjacency, while AND needs set intersection.")

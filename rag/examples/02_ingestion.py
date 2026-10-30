"""Conservative HTML text extraction for a tiny fixture; not a PDF parser."""
from html.parser import HTMLParser
from rag_core import Document, chunk_document, normalize

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.hidden = [], 0
    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden += 1
        if tag in {"p", "h1", "h2", "li", "br"} and not self.hidden:
            self.parts.append("\n")
    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden = max(0, self.hidden - 1)
        if tag in {"p", "h1", "h2", "li"} and not self.hidden:
            self.parts.append("\n")
    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

def extract(html):
    parser = TextExtractor()
    parser.feed(html)
    return normalize("".join(parser.parts))

if __name__ == "__main__":
    text = extract("<h1>休假</h1><p>特休提前三個工作日申請。</p><script>SECRET</script>")
    doc = Document("html-1", "示範頁面", text, source="demo://sample.html")
    for chunk in chunk_document(doc):
        print(chunk.doc_id, chunk.start, chunk.end, repr(chunk.text))

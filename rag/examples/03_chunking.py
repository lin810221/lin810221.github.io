"""All offsets and size values below count Python Unicode characters."""
from rag_core import Document, chunk_document

if __name__ == "__main__":
    doc = Document("chunk-demo", "切塊實驗", "申請特休須提前三個工作日。核准人是直屬主管。病假須當日通知。")
    for overlap in (0, 6):
        print(f"overlap={overlap}")
        for chunk in chunk_document(doc, size=18, overlap=overlap):
            print(f"  [{chunk.start}:{chunk.end}] {chunk.text}")

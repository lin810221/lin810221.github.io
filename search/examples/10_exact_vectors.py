"""Same vectors, eligibility and metric are prerequisites for ANN recall."""
from search_core import exact_topk,fixture_vector,fixtures

if __name__ == "__main__":
    docs = fixtures()
    vectors = [fixture_vector(d.title+" "+d.body) for d in docs]
    allowed = [i for i,d in enumerate(docs) if d.tenant=="alpha" and d.active]
    for index,score in exact_topk(vectors,fixture_vector("usb hub"),3,eligible=allowed):
        print(docs[index].doc_id,round(score,6))
    print("Features are handcrafted, not a learned embedding model.")

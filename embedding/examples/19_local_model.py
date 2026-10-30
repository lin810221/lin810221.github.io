"""Default dry run. Local model execution/download both require explicit flags."""
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--model-path", help="Use already downloaded model, network disabled")
    group.add_argument("--download-model", help="Explicitly allow downloading this model ID")
    parser.add_argument("--revision", help="Required pinned revision for a new download")
    parser.add_argument("--query-prefix", default=None, help="Override query prompt if the model card requires it")
    parser.add_argument("--document-prefix", default=None, help="Override document prompt if the model card requires it")
    args = parser.parse_args()
    if not args.model_path and not args.download_model:
        print("Dry run. Install sentence-transformers separately, then pass --model-path to run a local model.")
        print("A new download requires --download-model MODEL_ID --revision COMMIT_SHA.")
        return
    if args.download_model and not args.revision:
        parser.error("--download-model requires --revision to pin the model")
    if args.model_path and not Path(args.model_path).is_dir():
        parser.error("--model-path must exist")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(args.model_path or args.download_model, local_files_only=bool(args.model_path),
                                revision=args.revision, trust_remote_code=False)
    docs = ["向量與相似度", "網頁結構與樣式", "資料庫與索引"]
    document_vectors = model.encode_document(docs, prompt=args.document_prefix, normalize_embeddings=True)
    query_vector = model.encode_query(["如何比較兩個向量？"], prompt=args.query_prefix, normalize_embeddings=True)
    scores = model.similarity(query_vector, document_vectors)[0].tolist()
    print(sorted(zip(docs, scores), key=lambda row: -row[1]))

if __name__ == "__main__":
    main()

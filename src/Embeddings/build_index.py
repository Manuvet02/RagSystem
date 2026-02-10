import json
from pathlib import Path

import numpy as np

from src.Embeddings import Embedder , VectorStore

PROCESSED_DIR = Path("data/processed")
EMBEDDINGS_DIR = Path("data/embeddings")
INDEX_PATH = EMBEDDINGS_DIR / "faiss.index"


def build_index():
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    texts = []
    metadata = []

    for file_path in PROCESSED_DIR.glob("*.json"):
        data = json.loads(file_path.read_text(encoding="utf-8"))
        for idx,chunk in enumerate(data["chunks"]):
            texts.append(chunk)
            metadata.append({
                "document_id": data["document_id"],
                "filename": data["filename"],
                "chunk_index": idx
            })

    embedder = Embedder()
    embeddings = embedder.embed_texts(texts)

    vector_store = VectorStore(dimension=embeddings.shape[1])
    vector_store.add_embeddings(embeddings)
    vector_store.save(str(INDEX_PATH))

    metadata_path = EMBEDDINGS_DIR / "metadata.json"
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"FAISS index saved to {INDEX_PATH}")
    print(f"Metadata saved to {metadata_path}")


if __name__ == "__main__":
    build_index()

import json
from pathlib import Path
from typing import List, Dict

import numpy as np

from src.Embeddings import Embedder , VectorStore

EMBEDDINGS_DIR = Path("data/embeddings")
INDEX_PATH = EMBEDDINGS_DIR / "faiss.index"
METADATA_PATH = EMBEDDINGS_DIR / "metadata.json"


class Retriever:
    def __init__(self, top_k: int = 5):
        self.top_k = top_k
        self.embedder = Embedder()

        # Load FAISS index
        self.vector_store = VectorStore(dimension=384)
        self.vector_store.load(str(INDEX_PATH))

        # Load metadata
        self.metadata = json.loads(
            METADATA_PATH.read_text(encoding="utf-8")
        )

    def retrieve(self, query: str) -> List[Dict]:
        query_embedding = self.embedder.embed_texts([query])
        query_embedding = np.array(query_embedding)

        indices, distances = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=self.top_k
        )

        results = []
        for idx, distance in zip(indices, distances):
            meta = self.metadata[idx]
            results.append({
                "text_index": meta["chunk_index"],
                "distance": float(distance),
                "document_id": meta["document_id"],
                "filename": meta["filename"]
            })

        return results

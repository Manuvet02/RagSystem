from typing import List

from numpy import ndarray
from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: List[str]) -> ndarray:
        return self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )

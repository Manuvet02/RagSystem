import faiss
import numpy as np
from typing import List, Tuple


class VectorStore:
    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings: np.ndarray):
        self.index.add(embeddings)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> Tuple[List[int], List[float]]:
        distances, indices = self.index.search(query_embedding, top_k)
        return indices[0].tolist(), distances[0].tolist()

    def save(self, path: str):
        faiss.write_index(self.index, path)

    def load(self, path: str):
        self.index = faiss.read_index(path)

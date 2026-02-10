from src.Embeddings.vector_store import VectorStore

vs = VectorStore(dimension=384)
vs.load("Data/Embeddings/faiss.index")
print(vs.index.ntotal)  # numero di chunk caricati

from src.run_ingestion import ingest_document
from src.Embeddings.build_index import build_index

def run_pipeline():
    """
    Flusso completo RAG:
    1. Carica e pulisce i documenti
    2. Chunking e embeddings
    3. Salvataggio FAISS index
    """
    # Step 1: load, clean, chunk, embed
    ingest_document()

    # Step 2: build and save FAISS index
    build_index()

from pathlib import Path
from typing import List, Tuple

from src.Ingestion import load_document, clean_text , chunk_text
from src.NLP import preprocess_text , extract_entities
from src.Embeddings import Embedder , VectorStore

def run_pipeline(
    raw_dir: str,
    processed_dir: str,
    embeddings_dir: str,
    chunk_size: int = 300,
    stride: int = 50,
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
) -> Tuple[VectorStore, List[str], List[str]]:
    """
    Pipeline completa:
    1. Caricamento PDF
    2. Pulizia tecnica
    3. NLP Preprocessing + NER
    4. Chunking token-based
    5. Embeddings
    6. Creazione FAISS Vector Store
    """

    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)
    embeddings_dir = Path(embeddings_dir)

    processed_dir.mkdir(parents=True, exist_ok=True)
    embeddings_dir.mkdir(parents=True, exist_ok=True)

    print("Caricamento documenti PDF...")
    texts, filenames = load_document(raw_dir)

    all_chunks: List[str] = []
    all_metadata: List[str] = []

    print("Pulizia tecnica, NLP e chunking...")
    for text, fname in zip(texts, filenames):
        # Pulizia del file
        cleaned_text = clean_text(text)
        # 2️⃣ NLP preprocessing
        nlp_text = preprocess_text(cleaned_text)
        # 3️⃣ NER
        entities = extract_entities(cleaned_text)

        # Salvataggio entità
        entities_path = processed_dir / f"{fname}.entities.txt"
        with open(entities_path, "w", encoding="utf-8") as f:
            for label, values in entities.items():
                f.write(f"{label}: {set(values)}\n")

        #Token Chunk
        chunks = chunk_text(
            nlp_text,
            chunk_size=chunk_size,
            stride=stride
        )

        all_chunks.extend(chunks)
        all_metadata.extend([fname] * len(chunks))

        # Salva testo NLP pulito
        with open(processed_dir / fname, "w", encoding="utf-8") as f:
            f.write(nlp_text)

    print(f"🔹 Chunk totali creati: {len(all_chunks)}")

    # Generazione embeddings
    print("Generazione embeddings...")
    embedder = Embedder(model_name=embedding_model)
    embeddings = embedder.embed_texts(all_chunks)

    # Creazione Vector Store FAISS
    print("Creazione Vector Store...")
    vs = VectorStore(dimension=embeddings.shape[1])
    vs.add_embeddings(embeddings)
    vs.chunks = all_chunks

    vs.save(embeddings_dir/"faiss.index")

    # Salva metadata
    with open(embeddings_dir / "metadata.txt", "w", encoding="utf-8") as f:
        for m in all_metadata:
            f.write(m + "\n")

    print("Pipeline completata con successo")
    print(f"Embeddings indicizzati: {vs.index.ntotal}")

    return vs, all_chunks, all_metadata

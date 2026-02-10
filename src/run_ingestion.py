import json
import os
import uuid
from pathlib import Path

from Ingestion import load_document , clean_text , chunk_text

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")

def ingest_document() -> None:
    """Ingest documents from RAW_DATA_DIR and save processed JSON chunks"""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    files = list(RAW_DATA_DIR.iterdir())
    if not files:
        print(f"No files found in {RAW_DATA_DIR.resolve()}")
        return

    for file_path in files:
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in [".pdf", ".txt", ".docx"]:
            print(f"Ignoring unsupported file {file_path.name}")
            continue

        try :
            print(f"Ingesting {file_path.name}")
            text,metadata = load_document(file_path)

            if not text.strip():
                print(f"Warning: {file_path.name} produced empty text,skipping...")
                continue

            cleaned_text = clean_text(text)
            chunks = chunk_text(cleaned_text)

            if not chunks:
                print(f"Warning: {file_path.name} produced no chunks,skipping...")
                continue

            document_id = str(uuid.uuid4())

            output ={
                "document_id": document_id,
                "filename": file_path.name,
                "num_chunks": len(chunks),
                "chunks": chunks,
                "metadata": metadata
            }

            output_path = PROCESSED_DATA_DIR / f"{document_id}.json"
            with open(output_path, "w",encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)

            print(f"Saved {len(chunks)} chunks -> {output_path.name}")
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

if __name__ == "__main__":
    ingest_document()
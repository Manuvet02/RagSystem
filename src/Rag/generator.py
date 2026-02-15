from typing import List, Dict
from pathlib import Path
import json
from src.Rag.retriever import Retriever
import os
import ollama

# Percorso ai documenti processed
PROCESSED_DIR = Path("data/processed")

class Generator:
    def __init__(self, model_name: str = "mistral", top_k: int = 10):
        self.retriever = Retriever(top_k=top_k)
        self.model_name = model_name
        self.processed_cache = {}  # cache per recuperare i chunk reali

    def _load_chunk_text(self, document_id: str, chunk_index: int) -> str:
        """Recupera il testo reale di un chunk da processed JSON"""
        if document_id not in self.processed_cache:
            file_path = PROCESSED_DIR / f"{document_id}.json"
            data = json.loads(file_path.read_text(encoding="utf-8"))
            self.processed_cache[document_id] = data["chunks"]
        return self.processed_cache[document_id][chunk_index]

    def generate_answer(self, query: str) -> Dict:
        """
        Generate a response using RAG:
        1. Retrieve relevant chunks
        2. Send real text to Ollama/Mistral
        3. Return answer with sources
        """

        results = self.retriever.retrieve(query)
        sources = []
        context_texts = []

        for r in results:
            doc_id = r["document_id"]
            idx = r["text_index"]  # text_index dall'indice FAISS
            chunk_text = self._load_chunk_text(doc_id, idx)
            context_texts.append(chunk_text)
            sources.append(r["filename"])

        # Combina i chunk in un singolo prompt
        context_combined = "\n\n".join(context_texts)

        prompt = f"""
            You are an AI assistant skilled at extracting useful information from documents.
            Answer questions or queries using ONLY the information present in the context.
            If the context does not contain the answer, write: 'Information not available'
            
            CONTEXT:
            {context_combined}
            
            Answer the question below, citing the source filenames where possible.
            
            QUESTION:
            {query}
            """
        base_url = os.getenv("OLLAMA_BASE_URL","http://localhost:11434")
        client = ollama.Client(host=base_url)

        response = client.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
        return {
            "answer": response["message"]["content"],
            "sources": list(set(sources))
        }

# 🔹 Test rapido
if __name__ == "__main__":
    gen = Generator(top_k=10)
    query = "Is there anybody that is 'ASP.net web developer'?"
    result = gen.generate_answer(query)
    print("Answer:\n", result["answer"])
    print("Sources:\n", result["sources"])

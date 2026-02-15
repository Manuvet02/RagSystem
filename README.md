# RagSystem – Document Intelligence con RAG

**RagSystem** è un sistema di **document intelligence** basato su **RAG (Retrieval-Augmented Generation)** che permette di interrogare i tuoi documenti (PDF, DOCX, TXT) con un modello LLM tramite **FastAPI**.

---

## Funzionalità principali

- Caricamento e pulizia di documenti
- Suddivisione in chunk e creazione di embeddings con **SentenceTransformers**
- Indicizzazione semantica tramite **FAISS**
- Recupero intelligente dei documenti più rilevanti
- Risposte generate dal modello LLM (Ollama)
- API REST per interazioni e chat con il modello

---

## Esecuzione

### Locale
```bash
# Installazione dipendenze
pip install -r requirements.txt

#Avvio ingestion (prima volta)
python .\main.py ingest  

#Richiesta della query
python .\main.py query "Questa e' una query di prova"

#Avvio FastAPI(backend) per Frontend
python .\main.py serve
```
### Docker
```bash
docker compose build
docker compose up 
```

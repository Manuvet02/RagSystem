import argparse
import sys
from pathlib import Path

from src.Ingestion.pipeline import run_pipeline
from src.Rag.generator import Generator


RAW_DIR = Path("data/Raw")
PROCESSED_DIR = Path("data/Processed")
EMBEDDINGS_PATH = Path("data/Embeddings/faiss.index")


def run_ingestion():
    print("Starting ingestion pipeline...")
    run_pipeline()



def run_query(query: str):
    print("Running RAG...")
    generator = Generator()

    answer = generator.generate_answer(query)

    print("\n--- ANSWER ---\n")
    print(answer["answer"])
    print("\n--- RESOURCES ---\n")
    print(answer["sources"])

def run_api():
    import uvicorn
    uvicorn.run("src.API.main:app", host="127.0.0.1", port=8000, reload=True)


def main():
    parser = argparse.ArgumentParser(description="RAG Document Intelligence CLI")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("ingest", help="Run ingestion pipeline")
    subparsers.add_parser("serve", help="Start FastAPI server")

    query_parser = subparsers.add_parser("query", help="Run single RAG query")
    query_parser.add_argument("question", type=str, help="Query string")

    args = parser.parse_args()

    if args.command == "ingest":
        run_ingestion()
    elif args.command == "serve":
        run_api()
    elif args.command == "query":
        run_query(args.question)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

from pathlib import Path
from typing import Tuple, Dict
from pypdf import PdfReader
from docx import Document


def load_document(path: Path) -> Tuple[str, Dict]:
    """
    Load text from PDF, TXT, DOCX.
    Returns: (text, metadata)
    """

    if path.suffix.lower() == ".pdf":
        try:
            reader = PdfReader(path)
            texts = []

            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    # converte eventuali valori strani in stringa
                    texts.append(str(text))
            text = "\n".join(texts)
            metadata = {"type": "pdf", "pages": len(reader.pages)}

        except Exception as e:
            raise ValueError(f"Error reading PDF {path.name}: {e}")

    elif path.suffix.lower() == ".txt":
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            metadata = {"type": "txt"}
        except Exception as e:
            raise ValueError(f"Error reading TXT {path.name}: {e}")

    elif path.suffix.lower() == ".docx":
        try:
            doc = Document(path)
            text = "\n".join(p.text for p in doc.paragraphs)
            metadata = {"type": "docx"}
        except Exception as e:
            raise ValueError(f"Error reading DOCX {path.name}: {e}")

    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")

    if not text.strip():
        print(f"Warning: {path.name} produced empty text")

    return text, metadata

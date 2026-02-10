import re
from typing import List

STOPWORDS = {
    "e", "di", "a", "il", "la", "in", "per", "con", "su",
    "and", "the", "to", "of"
}

def preprocess_text(text: str) -> str:
    """Pulizia NLP base del testo"""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = text.split()

    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]

    return " ".join(tokens)
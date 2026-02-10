import spacy
from typing import Dict, List

nlp = spacy.load("en_core_web_md")

def extract_entities(text:str) -> Dict[str, List[str]]:
    """Estrae entità nominate dal testo"""
    doc = nlp(text)

    entities = {}
    for ent in doc.ents:
        entities.setdefault(ent.label_, []).append(ent.text)

    return entities
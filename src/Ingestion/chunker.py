from typing import List
from transformers import AutoTokenizer, PreTrainedTokenizer

# tokenizer compatibile con il modello embeddings
tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(
    'sentence-transformers/all-MiniLM-L6-v2'
)


def chunk_text(text: str, chunk_size: int = 300, stride: int = 50) -> List[str]:
    """
    Divide il testo in chunk basati sui token del modello embeddings.

    Args:
        text (str): testo completo da chunkare
        chunk_size (int): numero massimo di token per chunk
        stride (int): numero di token di sovrapposizione tra chunk consecutivi

    Returns:
        List[str]: lista di chunk come stringhe
    """
    if not text:
        return []

    # tokenizza tutto il testo
    tokens = tokenizer.tokenize(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end]

        # converte i token in stringa
        chunk_text = tokenizer.convert_tokens_to_string(chunk_tokens)
        chunks.append(chunk_text)

        # avanza di chunk_size - stride
        start += chunk_size - stride

    return chunks

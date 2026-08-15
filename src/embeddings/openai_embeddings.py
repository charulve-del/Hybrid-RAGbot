from typing import List

from openai import OpenAI

from src.config import OPENAI_API_KEY


EMBEDDING_MODEL = "text-embedding-3-small"


def create_embeddings(
    texts: List[str],
) -> List[List[float]]:

    if not texts:
        return []

    print(
        f"Creating embeddings for {len(texts)} texts..."
    )

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    embeddings = [
        item.embedding
        for item in response.data
    ]

    print(
        f"Embeddings created: "
        f"{len(embeddings)}"
    )

    if embeddings:

        print(
            f"Embedding dimension: "
            f"{len(embeddings[0])}"
        )

    return embeddings
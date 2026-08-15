import json

from langchain_openai import OpenAIEmbeddings

from src.config import (
    CHUNKS_FILE,
    OPENAI_API_KEY,
)


def main():

    print("=" * 60)
    print("BATCH EMBEDDING TEST")
    print("=" * 60)

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        chunks = json.load(f)

    print(
        f"Total chunks loaded: {len(chunks)}"
    )

    first_batch = chunks[:20]

    texts = [
        chunk["text"]
        for chunk in first_batch
    ]

    print(
        f"Texts in batch: {len(texts)}"
    )

    print("\nCreating embeddings client...")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=OPENAI_API_KEY,
    )

    print("Embeddings client ready.")

    print(
        "\nSending 20 texts to OpenAI..."
    )

    try:

        vectors = embeddings.embed_documents(
            texts
        )

        print("\nSUCCESS!")

        print(
            "Number of vectors:",
            len(vectors),
        )

        print(
            "Vector dimension:",
            len(vectors[0]),
        )

    except Exception as e:

        print("\nERROR!")

        print(
            "Exception type:",
            type(e).__name__,
        )

        print(
            "Exception:",
            str(e),
        )

        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
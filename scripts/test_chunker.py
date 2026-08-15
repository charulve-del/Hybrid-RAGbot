import json

from src.ingestion.loaders import load_documents
from src.ingestion.chunker import chunk_document


def main():

    documents = load_documents("data/raw")

    all_chunks = []

    for document in documents:

        chunks = chunk_document(document)

        print("=" * 60)
        print(f"Document: {document['source']}")
        print(f"Pages: {document['page_count']}")
        print(f"Chunks: {len(chunks)}")

        if chunks:
            first_chunk = chunks[0]

            print("\nFirst chunk:")
            print(first_chunk.text[:500])

            print("\nMetadata:")
            print(first_chunk.model_dump())

        all_chunks.extend(chunks)

    output = [
        chunk.model_dump()
        for chunk in all_chunks
    ]

    with open(
        "data/processed/chunks/chunks.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"\nTotal chunks created: {len(all_chunks)}"
    )


if __name__ == "__main__":
    main()
import json
from pathlib import Path

from src.ingestion.loaders import load_documents


def main():
    documents = load_documents("data/raw")

    print(f"\nLoaded {len(documents)} documents\n")

    for document in documents:
        print("=" * 60)
        print(f"Document:   {document['document_id']}")
        print(f"Source:     {document['source']}")
        print(f"Department: {document['department']}")
        print(f"Pages:      {document['page_count']}")

        if document["pages"]:
            first_page = document["pages"][0]

            print("\nFirst page:")
            print(first_page["text"][:500])

    output_path = Path(
        "data/processed/documents/loaded_documents.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            documents,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\nSaved processed documents to: {output_path}")


if __name__ == "__main__":
    main()
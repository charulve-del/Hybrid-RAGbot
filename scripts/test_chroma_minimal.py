import chromadb

from src.config import CHROMA_DIR


def main():

    print("=" * 60)
    print("MINIMAL CHROMA TEST")
    print("=" * 60)

    print("\nChroma path:")
    print(CHROMA_DIR)

    print("\nCreating PersistentClient...")

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    print("Client created.")

    print("\nCreating collection...")

    collection = client.get_or_create_collection(
        name="minimal_test"
    )

    print("Collection created.")

    print("\nAdding ONE vector...")

    try:

        collection.add(
            ids=["test-1"],
            embeddings=[
                [0.1, 0.2, 0.3, 0.4]
            ],
            documents=[
                "This is a Chroma test document."
            ],
            metadatas=[
                {
                    "test": "true"
                }
            ],
        )

        print("ONE VECTOR INSERTED SUCCESSFULLY.")

    except Exception as e:

        print("\nCHROMA ERROR")

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

        return

    print("\nReading test vector...")

    result = collection.get(
        ids=["test-1"]
    )

    print(
        "Returned IDs:",
        result["ids"],
    )

    print("\n" + "=" * 60)
    print("MINIMAL CHROMA TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
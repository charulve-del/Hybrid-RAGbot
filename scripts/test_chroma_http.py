import chromadb


def main():

    print("=" * 60)
    print("CHROMA CLIENT TEST")
    print("=" * 60)

    print("\nCreating in-memory Chroma client...")

    client = chromadb.EphemeralClient()

    print("Client created.")

    print("\nCreating collection...")

    collection = client.get_or_create_collection(
        name="test_collection"
    )

    print("Collection created.")

    print("\nAdding ONE vector...")

    collection.add(
        ids=["test1"],
        embeddings=[
            [0.1, 0.2, 0.3, 0.4]
        ],
        documents=[
            "This is a test document."
        ],
    )

    print("Vector inserted successfully.")

    print("\nQuerying vector...")

    result = collection.query(
        query_embeddings=[
            [0.1, 0.2, 0.3, 0.4]
        ],
        n_results=1,
    )

    print("Query successful.")

    print("\nResult:")
    print(result)

    print("\n" + "=" * 60)
    print("CHROMA TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
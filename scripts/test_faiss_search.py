from src.vector_store.faiss_store import (
    FAISSVectorStore,
)


def main():

    print("=" * 60)
    print("FAISS VECTOR SEARCH TEST")
    print("=" * 60)

    store = FAISSVectorStore()

    # ------------------------------------------
    # Load index + metadata
    # ------------------------------------------

    store.load()

    # ------------------------------------------
    # Get question
    # ------------------------------------------

    question = input(
        "\nEnter your policy question: "
    ).strip()

    if not question:

        print(
            "Question cannot be empty."
        )

        return

    # ------------------------------------------
    # Search
    # ------------------------------------------

    print(
        "\nSearching FAISS..."
    )

    results = store.search(
        question,
        k=5,
    )

    # ------------------------------------------
    # Display results
    # ------------------------------------------

    print("\n" + "=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)

    print(
        f"\nResults returned: {len(results)}"
    )

    for i, result in enumerate(
        results,
        start=1,
    ):

        print(
            f"\n--- RESULT {i} ---"
        )

        print(
            "Chunk ID:",
            result.get("chunk_id"),
        )

        print(
            "Document ID:",
            result.get("document_id"),
        )

        print(
            "Source:",
            result.get("source"),
        )

        print(
            "Page:",
            result.get("page_start"),
            "-",
            result.get("page_end"),
        )

        print(
            "Distance:",
            result.get("distance"),
        )

        print(
            "Retrieval source:",
            result.get(
                "retrieval_source"
            ),
        )

        print("\nText:")

        print(
            result.get(
                "text",
                "",
            )[:1000]
        )

    print("\n" + "=" * 60)
    print("FAISS SEARCH TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
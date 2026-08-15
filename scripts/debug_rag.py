from src.retrieval.hybrid_retriever import (
    HybridRetriever,
)


def main():

    print("=" * 70)
    print("HYBRID RAG DEBUG")
    print("=" * 70)

    question = input(
        "\nEnter question: "
    ).strip()

    retriever = HybridRetriever(
        vector_k=5,
        graph_k=5,
    )

    try:

        result = retriever.retrieve(
            question
        )

        print(
            "\n" + "=" * 70
        )

        print(
            "FAISS RESULTS"
        )

        print(
            "=" * 70
        )

        for index, item in enumerate(
            result[
                "vector_results"
            ],
            start=1,
        ):

            print(
                f"\n[{index}]"
            )

            print(
                "Chunk:",
                item.get(
                    "chunk_id"
                ),
            )

            print(
                "Distance:",
                item.get(
                    "distance"
                ),
            )

            print(
                "Source:",
                item.get(
                    "source"
                ),
            )

            print(
                "Text:",
                item.get(
                    "text",
                    "",
                )[:500],
            )

        print(
            "\n" + "=" * 70
        )

        print(
            "GRAPH RESULTS"
        )

        print(
            "=" * 70
        )

        print(
            "\nEntities:"
        )

        for entity in result[
            "graph_entities"
        ]:

            print(entity)

        print(
            "\nRelationships:"
        )

        for relationship in result[
            "graph_relationships"
        ]:

            print(relationship)

        print(
            "\nGraph chunks:"
        )

        for chunk in result[
            "graph_chunks"
        ]:

            print(
                chunk
            )

        print(
            "\n" + "=" * 70
        )

        print(
            "MERGED CHUNKS"
        )

        print(
            "=" * 70
        )

        for index, chunk in enumerate(
            result[
                "merged_chunks"
            ],
            start=1,
        ):

            print(
                f"\n[{index}] "
                f"{chunk.get('chunk_id')}"
            )

            print(
                "Retrieval source:",
                chunk.get(
                    "retrieval_source"
                ),
            )

            print(
                chunk.get(
                    "text",
                    "",
                )[:700]
            )

    finally:

        retriever.close()


if __name__ == "__main__":
    main()
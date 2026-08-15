from src.retrieval.hybrid_retriever import (
    HybridRetriever,
)


def main():

    print("=" * 60)
    print("HYBRID RETRIEVER TEST")
    print("=" * 60)

    retriever = None

    try:

        retriever = HybridRetriever(
            vector_k=5,
            graph_k=5,
        )

        question = input(
            "\nEnter your policy question: "
        ).strip()

        if not question:

            print(
                "Question cannot be empty."
            )

            return

        result = retriever.retrieve(
            question
        )

        # ------------------------------------------
        # FAISS
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("FAISS RESULTS")
        print("=" * 60)

        for i, result_item in enumerate(
            result["vector_results"],
            start=1,
        ):

            print(
                f"\n--- VECTOR RESULT {i} ---"
            )

            print(
                "Chunk:",
                result_item.get(
                    "chunk_id"
                ),
            )

            print(
                "Source:",
                result_item.get(
                    "source"
                ),
            )

            print(
                "Page:",
                result_item.get(
                    "page_start"
                ),
            )

            print(
                "Distance:",
                result_item.get(
                    "distance"
                ),
            )

            print(
                "Text:"
            )

            print(
                result_item.get(
                    "text",
                    "",
                )[:500]
            )

        # ------------------------------------------
        # GRAPH
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("NEO4J ENTITIES")
        print("=" * 60)

        for entity in result[
            "graph_entities"
        ]:

            print(
                f"- "
                f"{entity['name']} "
                f"[{entity['entity_type']}]"
            )

        print("\n" + "=" * 60)
        print("NEO4J RELATIONSHIPS")
        print("=" * 60)

        for relationship in result[
            "graph_relationships"
        ]:

            print(
                f"- "
                f"{relationship['source']} "
                f"--"
                f"{relationship['relationship']}"
                f"--> "
                f"{relationship['target']}"
            )

        # ------------------------------------------
        # MERGED
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("MERGED HYBRID RESULTS")
        print("=" * 60)

        print(
            "\nTotal merged chunks:",
            len(
                result[
                    "merged_chunks"
                ]
            ),
        )

        for i, chunk in enumerate(
            result[
                "merged_chunks"
            ],
            start=1,
        ):

            print(
                f"\n--- HYBRID RESULT {i} ---"
            )

            print(
                "Chunk:",
                chunk.get(
                    "chunk_id"
                ),
            )

            print(
                "Retrieval source:",
                chunk.get(
                    "retrieval_source"
                ),
            )

            print(
                "Source:",
                chunk.get(
                    "source"
                ),
            )

            print(
                "Page:",
                chunk.get(
                    "page_start"
                ),
            )

            print(
                "Text:"
            )

            print(
                chunk.get(
                    "text",
                    "",
                )[:500]
            )

        print("\n" + "=" * 60)
        print(
            "HYBRID RETRIEVER TEST COMPLETE"
        )
        print("=" * 60)

    except Exception as e:

        print(
            "\nHybrid retrieval failed."
        )

        print(
            "Exception type:",
            type(e).__name__,
        )

        print(
            "Exception:",
            str(e),
        )

    finally:

        if retriever:

            retriever.close()


if __name__ == "__main__":
    main()
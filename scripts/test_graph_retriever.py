from src.retrieval.graph_retriever import (
    GraphRetriever,
)


def main():

    print("=" * 60)
    print("GRAPH RETRIEVER TEST")
    print("=" * 60)

    retriever = None

    try:

        retriever = GraphRetriever()

        keyword = input(
            "\nEnter graph search keyword: "
        ).strip()

        if not keyword:

            print(
                "Keyword cannot be empty."
            )

            return

        result = retriever.retrieve(
            keyword,
            entity_limit=5,
            relationship_limit=10,
            chunk_limit=5,
        )

        # ------------------------------------------
        # Entities
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("ENTITIES")
        print("=" * 60)

        print(
            "Count:",
            len(result["entities"]),
        )

        for entity in result[
            "entities"
        ]:

            print(
                f"\nName: "
                f"{entity['name']}"
            )

            print(
                f"Type: "
                f"{entity['entity_type']}"
            )

            print(
                f"Properties: "
                f"{entity['properties']}"
            )

        # ------------------------------------------
        # Relationships
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("RELATIONSHIPS")
        print("=" * 60)

        print(
            "Count:",
            len(
                result[
                    "relationships"
                ]
            ),
        )

        for relationship in result[
            "relationships"
        ]:

            print(
                f"\n"
                f"{relationship['source']} "
                f"--"
                f"{relationship['relationship']}"
                f"--> "
                f"{relationship['target']}"
            )

        # ------------------------------------------
        # Chunks
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("CHUNKS")
        print("=" * 60)

        print(
            "Count:",
            len(
                result["chunks"]
            ),
        )

        for chunk in result[
            "chunks"
        ]:

            print(
                f"\nChunk ID: "
                f"{chunk['chunk_id']}"
            )

            print(
                f"Source: "
                f"{chunk.get('source')}"
            )

            print(
                f"Page: "
                f"{chunk.get('page_start')}"
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
        print("GRAPH RETRIEVER TEST COMPLETE")
        print("=" * 60)

    except Exception as e:

        print(
            "\nGraph retrieval failed."
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
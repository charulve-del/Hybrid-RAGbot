from neo4j import GraphDatabase

from src.config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)


def search_chunks(
    session,
    department=None,
    document_type=None,
    limit=5,
):
    """
    Retrieve chunks from Neo4j using graph metadata.
    """

    query = """
    MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk)
    OPTIONAL MATCH (d)-[:BELONGS_TO]->(dept:Department)
    OPTIONAL MATCH (d)-[:HAS_TYPE]->(dtype:DocumentType)

    WHERE
        ($department IS NULL OR dept.name = $department)
        AND
        ($document_type IS NULL OR dtype.name = $document_type)

    RETURN
        d.document_id AS document_id,
        d.source AS source,
        d.department AS department,
        d.document_type AS document_type,
        c.chunk_id AS chunk_id,
        c.text AS text,
        c.page_start AS page_start,
        c.page_end AS page_end

    LIMIT $limit
    """

    result = session.run(
        query,
        department=department,
        document_type=document_type,
        limit=limit,
    )

    return list(result)


def main():

    print("=" * 60)
    print("NEO4J GRAPH SEARCH TEST")
    print("=" * 60)

    print("\nConnecting to Neo4j...")

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(
            NEO4J_USERNAME,
            NEO4J_PASSWORD,
        ),
    )

    try:

        driver.verify_connectivity()

        print(
            "Neo4j connection successful."
        )

        with driver.session() as session:

            # ----------------------------------------
            # Show graph counts
            # ----------------------------------------

            print(
                "\nChecking graph..."
            )

            result = session.run(
                """
                MATCH (n)
                RETURN count(n) AS node_count
                """
            )

            record = result.single()

            print(
                "Total nodes:",
                record["node_count"],
            )

            result = session.run(
                """
                MATCH ()-[r]->()
                RETURN count(r) AS relationship_count
                """
            )

            record = result.single()

            print(
                "Total relationships:",
                record["relationship_count"],
            )

            # ----------------------------------------
            # Ask question
            # ----------------------------------------

            question = input(
                "\nEnter your policy question: "
            ).strip()

            if not question:

                print(
                    "Question cannot be empty."
                )

                return

            print(
                f"\nQuestion: {question}"
            )

            # ----------------------------------------
            # Initial graph retrieval
            #
            # At this stage we retrieve chunks.
            # Semantic ranking will be added later.
            # ----------------------------------------

            print(
                "\nRetrieving chunks from Neo4j..."
            )

            records = search_chunks(
                session,
                limit=5,
            )

            # ----------------------------------------
            # Display
            # ----------------------------------------

            print("\n" + "=" * 60)
            print("GRAPH SEARCH RESULTS")
            print("=" * 60)

            for rank, record in enumerate(
                records,
                start=1,
            ):

                print(
                    f"\n{'-' * 60}"
                )

                print(
                    f"RESULT #{rank}"
                )

                print(
                    "Document ID:",
                    record["document_id"],
                )

                print(
                    "Chunk ID:",
                    record["chunk_id"],
                )

                print(
                    "Source:",
                    record["source"],
                )

                print(
                    "Department:",
                    record["department"],
                )

                print(
                    "Document Type:",
                    record["document_type"],
                )

                print(
                    "Page:",
                    record["page_start"],
                    "-",
                    record["page_end"],
                )

                print("\nText:")

                print(
                    record["text"]
                )

            print(
                "\n" + "=" * 60
            )

    except Exception as e:

        print(
            "\nNeo4j search failed."
        )

        print(
            "Exception:",
            type(e).__name__,
        )

        print(
            "Message:",
            str(e),
        )

    finally:

        driver.close()

    print(
        "\nNeo4j search test complete."
    )


if __name__ == "__main__":
    main()
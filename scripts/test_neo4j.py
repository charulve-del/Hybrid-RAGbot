from neo4j import GraphDatabase

from src.config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)


def main():

    print("=" * 60)
    print("NEO4J CONNECTION TEST")
    print("=" * 60)

    print("\nNeo4j URI:")
    print(NEO4J_URI)

    print("\nNeo4j username:")
    print(NEO4J_USERNAME)

    print("\nChecking password...")

    if not NEO4J_PASSWORD:
        print("ERROR: NEO4J_PASSWORD is not loaded.")
        return

    print("Password loaded.")

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
            "\nSUCCESS!"
        )

        print(
            "Neo4j connection established."
        )

        with driver.session() as session:

            result = session.run(
                "RETURN 1 AS result"
            )

            record = result.single()

            print(
                "Test query result:",
                record["result"],
            )

    except Exception as e:

        print(
            "\nNEO4J CONNECTION FAILED"
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

        driver.close()

        print(
            "\nNeo4j driver closed."
        )

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
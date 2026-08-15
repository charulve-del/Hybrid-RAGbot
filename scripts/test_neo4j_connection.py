from neo4j import GraphDatabase

from src.config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)


print("=" * 60)
print("NEO4J CONNECTION TEST")
print("=" * 60)

print("URI:", NEO4J_URI)
print("Username:", NEO4J_USERNAME)
print("Password configured:", bool(NEO4J_PASSWORD))

driver = None

try:

    print("\nCreating driver...")

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(
            NEO4J_USERNAME,
            NEO4J_PASSWORD,
        ),
    )

    print("Driver created.")

    print("\nVerifying connectivity...")

    driver.verify_connectivity()

    print("Neo4j connectivity SUCCESS!")

    with driver.session() as session:

        result = session.run(
            "RETURN 1 AS result"
        )

        record = result.single()

        print(
            "Query result:",
            record["result"],
        )

except Exception as e:

    print("\nNeo4j connection FAILED.")

    print(
        "Exception type:",
        type(e).__name__,
    )

    print(
        "Exception:",
        str(e),
    )

finally:

    if driver:

        driver.close()

print("\nTest complete.")
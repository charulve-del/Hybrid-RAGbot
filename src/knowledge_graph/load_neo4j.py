import json
from pathlib import Path

from neo4j import GraphDatabase

from src.config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)


EXTRACTIONS_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "knowledge_graph"
    / "extractions.json"
)


def load_extractions():

    print("\nLoading extractions...")

    with open(
        EXTRACTIONS_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        data = json.load(f)

    print(
        f"Loaded extraction records: {len(data)}"
    )

    return data


def create_constraints(session):

    print("\nCreating constraints...")

    queries = [

        """
        CREATE CONSTRAINT entity_unique
        IF NOT EXISTS
        FOR (e:Entity)
        REQUIRE e.key IS UNIQUE
        """,

        """
        CREATE CONSTRAINT chunk_unique
        IF NOT EXISTS
        FOR (c:Chunk)
        REQUIRE c.chunk_id IS UNIQUE
        """,

    ]

    for query in queries:
        session.run(query)

    print("Constraints ready.")


def create_chunk(
    session,
    record,
):

    query = """
    MERGE (c:Chunk {
        chunk_id: $chunk_id
    })

    SET
        c.document_id = $document_id,
        c.source = $source,
        c.file_path = $file_path,
        c.department = $department,
        c.document_type = $document_type,
        c.page_start = $page_start,
        c.page_end = $page_end
    """

    session.run(
        query,
        chunk_id=record["chunk_id"],
        document_id=record["document_id"],
        source=record["source"],
        file_path=record["file_path"],
        department=record["department"],
        document_type=record["document_type"],
        page_start=record["page_start"],
        page_end=record["page_end"],
    )


def create_entity(
    session,
    entity,
    chunk_id,
):

    entity_name = entity["name"].strip()
    entity_type = entity["entity_type"].strip()

    if not entity_name:
        return

    # We create a stable key so that the same
    # entity mentioned in many chunks becomes
    # one Neo4j node.

    entity_key = (
        f"{entity_type.lower()}:"
        f"{entity_name.lower()}"
    )

    query = """
    MERGE (e:Entity {
        key: $key
    })

    SET
        e.name = $name,
        e.entity_type = $entity_type

    WITH e

    MATCH (c:Chunk {
        chunk_id: $chunk_id
    })

    MERGE (c)-[:MENTIONS]->(e)
    """

    session.run(
        query,
        key=entity_key,
        name=entity_name,
        entity_type=entity_type,
        chunk_id=chunk_id,
    )


def create_relationship(
    session,
    relationship,
    chunk_id,
):

    source_name = relationship[
        "source"
    ].strip()

    source_type = relationship[
        "source_type"
    ].strip()

    target_name = relationship[
        "target"
    ].strip()

    target_type = relationship[
        "target_type"
    ].strip()

    relation_type = relationship[
        "relationship"
    ].strip().upper()

    if (
        not source_name
        or not target_name
        or not relation_type
    ):
        return

    source_key = (
        f"{source_type.lower()}:"
        f"{source_name.lower()}"
    )

    target_key = (
        f"{target_type.lower()}:"
        f"{target_name.lower()}"
    )

    query = f"""
    MATCH (source:Entity {{
        key: $source_key
    }})

    MATCH (target:Entity {{
        key: $target_key
    }})

    MERGE (source)-[r:{relation_type}]->(target)

    SET
        r.source_chunk_id = $chunk_id
    """

    session.run(
        query,
        source_key=source_key,
        target_key=target_key,
        chunk_id=chunk_id,
    )


def main():

    print("=" * 60)
    print("LOADING KNOWLEDGE GRAPH INTO NEO4J")
    print("=" * 60)

    records = load_extractions()

    print(
        "\nConnecting to Neo4j..."
    )

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

            create_constraints(
                session
            )

            total_entities = 0
            total_relationships = 0

            total_records = len(records)

            for i, record in enumerate(
                records,
                start=1,
            ):

                # ----------------------------------
                # Chunk
                # ----------------------------------

                create_chunk(
                    session,
                    record,
                )

                extraction = record.get(
                    "extraction",
                    {},
                )

                entities = extraction.get(
                    "entities",
                    [],
                )

                relationships = extraction.get(
                    "relationships",
                    [],
                )

                # ----------------------------------
                # Entities
                # ----------------------------------

                for entity in entities:

                    create_entity(
                        session,
                        entity,
                        record["chunk_id"],
                    )

                    total_entities += 1

                # ----------------------------------
                # Relationships
                # ----------------------------------

                for relationship in relationships:

                    create_relationship(
                        session,
                        relationship,
                        record["chunk_id"],
                    )

                    total_relationships += 1

                if (
                    i % 20 == 0
                    or i == total_records
                ):

                    print(
                        f"Processed "
                        f"{i}/{total_records} "
                        f"chunks | "
                        f"entities: "
                        f"{total_entities} | "
                        f"relationships: "
                        f"{total_relationships}"
                    )

    finally:

        driver.close()

    print("\n" + "=" * 60)
    print("KNOWLEDGE GRAPH LOAD COMPLETE")
    print("=" * 60)

    print(
        f"\nEntity mentions processed: "
        f"{total_entities}"
    )

    print(
        f"Relationships processed: "
        f"{total_relationships}"
    )


if __name__ == "__main__":
    main()
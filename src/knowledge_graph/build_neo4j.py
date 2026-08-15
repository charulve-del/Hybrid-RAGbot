import json

from neo4j import GraphDatabase

from src.config import (
    CHUNKS_FILE,
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)


def load_chunks():

    print("\nLoading chunks...")

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        chunks = json.load(f)

    print(
        f"Loaded chunks: {len(chunks)}"
    )

    return chunks


def create_constraints(session):

    print("\nCreating constraints...")

    queries = [

        """
        CREATE CONSTRAINT document_id_unique IF NOT EXISTS
        FOR (d:Document)
        REQUIRE d.document_id IS UNIQUE
        """,

        """
        CREATE CONSTRAINT chunk_id_unique IF NOT EXISTS
        FOR (c:Chunk)
        REQUIRE c.chunk_id IS UNIQUE
        """,

        """
        CREATE CONSTRAINT department_name_unique IF NOT EXISTS
        FOR (d:Department)
        REQUIRE d.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT document_type_name_unique IF NOT EXISTS
        FOR (t:DocumentType)
        REQUIRE t.name IS UNIQUE
        """,
    ]

    for query in queries:

        session.run(query)

    print("Constraints created.")


def create_document_graph(session, chunks):

    print(
        "\nCreating document/chunk graph..."
    )

    query = """
    MERGE (d:Document {
        document_id: $document_id
    })

    SET
        d.source = $source,
        d.file_path = $file_path,
        d.department = $department,
        d.document_type = $document_type,
        d.title = $title,
        d.version = $version,
        d.effective_date = $effective_date

    MERGE (c:Chunk {
        chunk_id: $chunk_id
    })

    SET
        c.document_id = $document_id,
        c.text = $text,
        c.page_start = $page_start,
        c.page_end = $page_end,
        c.chunk_index = $chunk_index,
        c.section = $section

    MERGE (d)-[:HAS_CHUNK]->(c)

    MERGE (dept:Department {
        name: $department
    })

    MERGE (d)-[:BELONGS_TO]->(dept)

    MERGE (dtype:DocumentType {
        name: $document_type
    })

    MERGE (d)-[:HAS_TYPE]->(dtype)
    """

    for i, chunk in enumerate(chunks, start=1):

        session.run(
            query,
            document_id=chunk["document_id"],
            source=chunk["source"],
            file_path=chunk["file_path"],
            department=chunk["department"],
            document_type=chunk.get(
                "document_type",
                "unknown",
            ),
            title=chunk.get("title"),
            version=chunk.get("version"),
            effective_date=chunk.get(
                "effective_date"
            ),
            chunk_id=chunk["chunk_id"],
            text=chunk["text"],
            page_start=chunk["page_start"],
            page_end=chunk["page_end"],
            chunk_index=chunk["chunk_index"],
            section=chunk.get("section"),
        )

        if i % 20 == 0 or i == len(chunks):

            print(
                f"Processed {i}/{len(chunks)} chunks"
            )


def create_supersedes_relationships(
    session,
    chunks,
):

    print(
        "\nCreating document version relationships..."
    )

    query = """
    MATCH (old:Document {
        document_id: $old_document_id
    })

    MATCH (new:Document {
        document_id: $new_document_id
    })

    MERGE (new)-[:SUPERSEDES]->(old)
    """

    count = 0

    for chunk in chunks:

        old_document_id = chunk.get(
            "supersedes_document_id"
        )

        if not old_document_id:
            continue

        session.run(
            query,
            old_document_id=old_document_id,
            new_document_id=chunk[
                "document_id"
            ],
        )

        count += 1

    print(
        f"Supersedes relationships created: "
        f"{count}"
    )


def main():

    print("=" * 60)
    print("BUILDING NEO4J KNOWLEDGE GRAPH")
    print("=" * 60)

    chunks = load_chunks()

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

            # ----------------------------------
            # Constraints
            # ----------------------------------

            create_constraints(
                session
            )

            # ----------------------------------
            # Main graph
            # ----------------------------------

            create_document_graph(
                session,
                chunks,
            )

            # ----------------------------------
            # Version relationships
            # ----------------------------------

            create_supersedes_relationships(
                session,
                chunks,
            )

    finally:

        driver.close()

    print("\n" + "=" * 60)
    print("NEO4J GRAPH BUILD COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
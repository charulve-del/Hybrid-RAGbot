from typing import Any, Dict, List

from neo4j import GraphDatabase

from src.config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)


class GraphRetriever:

    def __init__(self):

        print("Creating Neo4j driver...")

        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(
                NEO4J_USERNAME,
                NEO4J_PASSWORD,
            ),
        )

        self.driver.verify_connectivity()

        print("Neo4j connection successful.")

    # --------------------------------------------------
    # Close
    # --------------------------------------------------

    def close(self):

        if self.driver:
            self.driver.close()

    # --------------------------------------------------
    # Main retrieval
    # --------------------------------------------------

    def retrieve(
        self,
        keyword: str,
        entity_limit: int = 5,
        relationship_limit: int = 10,
        chunk_limit: int = 5,
    ) -> Dict[str, List[Dict[str, Any]]]:

        with self.driver.session() as session:

            entities = session.execute_read(
                self._find_entities,
                keyword,
                entity_limit,
            )

            relationships = session.execute_read(
                self._find_relationships,
                keyword,
                relationship_limit,
            )

            chunks = session.execute_read(
                self._find_chunks,
                keyword,
                chunk_limit,
            )

        return {
            "entities": entities,
            "relationships": relationships,
            "chunks": chunks,
        }

    # --------------------------------------------------
    # Find entities
    # --------------------------------------------------

    @staticmethod
    def _find_entities(
        tx,
        keyword: str,
        limit: int,
    ):

        query = """
        MATCH (n)
        WHERE
            any(
                key IN keys(n)
                WHERE
                    toLower(
                        toString(
                            n[key]
                        )
                    )
                    CONTAINS
                    toLower($keyword)
            )
        RETURN
            elementId(n) AS node_id,
            labels(n) AS labels,
            properties(n) AS properties
        LIMIT $limit
        """

        result = tx.run(
            query,
            keyword=keyword,
            limit=limit,
        )

        entities = []

        for record in result:

            properties = record["properties"]
            labels = record["labels"]

            name = (
                properties.get("name")
                or properties.get("title")
                or properties.get("entity")
                or properties.get("chunk_id")
                or record["node_id"]
            )

            entity_type = (
                labels[0]
                if labels
                else "Entity"
            )

            entities.append(
                {
                    "node_id": record["node_id"],
                    "name": str(name),
                    "entity_type": entity_type,
                    "properties": properties,
                }
            )

        return entities

    # --------------------------------------------------
    # Find relationships
    # --------------------------------------------------

    @staticmethod
    def _find_relationships(
        tx,
        keyword: str,
        limit: int,
    ):

        query = """
        MATCH (a)-[r]->(b)
        WHERE
            any(
                key IN keys(a)
                WHERE
                    toLower(
                        toString(
                            a[key]
                        )
                    )
                    CONTAINS
                    toLower($keyword)
            )
            OR
            any(
                key IN keys(b)
                WHERE
                    toLower(
                        toString(
                            b[key]
                        )
                    )
                    CONTAINS
                    toLower($keyword)
            )
        RETURN
            properties(a) AS source_properties,
            labels(a) AS source_labels,
            type(r) AS relationship,
            properties(b) AS target_properties,
            labels(b) AS target_labels
        LIMIT $limit
        """

        result = tx.run(
            query,
            keyword=keyword,
            limit=limit,
        )

        relationships = []

        for record in result:

            source_properties = (
                record["source_properties"]
            )

            target_properties = (
                record["target_properties"]
            )

            source_name = (
                source_properties.get("name")
                or source_properties.get("title")
                or source_properties.get("entity")
                or source_properties.get("chunk_id")
                or str(source_properties)
            )

            target_name = (
                target_properties.get("name")
                or target_properties.get("title")
                or target_properties.get("entity")
                or target_properties.get("chunk_id")
                or str(target_properties)
            )

            relationships.append(
                {
                    "source": str(source_name),
                    "source_type": (
                        record["source_labels"][0]
                        if record["source_labels"]
                        else "Entity"
                    ),
                    "relationship": record[
                        "relationship"
                    ],
                    "target": str(target_name),
                    "target_type": (
                        record["target_labels"][0]
                        if record["target_labels"]
                        else "Entity"
                    ),
                }
            )

        return relationships

    # --------------------------------------------------
    # Find chunks
    # --------------------------------------------------

    @staticmethod
    def _find_chunks(
        tx,
        keyword: str,
        limit: int,
    ):

        query = """
        MATCH (n)
        WHERE
            (
                "Chunk" IN labels(n)
                OR
                "DocumentChunk" IN labels(n)
            )
            AND
            any(
                key IN keys(n)
                WHERE
                    toLower(
                        toString(
                            n[key]
                        )
                    )
                    CONTAINS
                    toLower($keyword)
            )
        RETURN properties(n) AS properties
        LIMIT $limit
        """

        result = tx.run(
            query,
            keyword=keyword,
            limit=limit,
        )

        chunks = []

        for record in result:

            properties = record["properties"]

            chunk_id = properties.get(
                "chunk_id"
            )

            if not chunk_id:
                continue

            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "document_id": properties.get(
                        "document_id"
                    ),
                    "source": properties.get(
                        "source"
                    ),
                    "file_path": properties.get(
                        "file_path"
                    ),
                    "department": properties.get(
                        "department"
                    ),
                    "document_type": properties.get(
                        "document_type"
                    ),
                    "page_start": properties.get(
                        "page_start"
                    ),
                    "page_end": properties.get(
                        "page_end"
                    ),
                    "section": properties.get(
                        "section"
                    ),
                    "title": properties.get(
                        "title"
                    ),
                    "text": properties.get(
                        "text",
                        "",
                    ),
                    "retrieval_source": "graph",
                }
            )

        return chunks
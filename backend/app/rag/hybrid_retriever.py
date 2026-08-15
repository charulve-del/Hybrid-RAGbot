from typing import Any, Dict, List

from src.vector_store.faiss_store import FAISSVectorStore
from src.retrieval.graph_retriever import GraphRetriever


class HybridRetriever:

    def __init__(
        self,
        vector_k: int = 5,
        graph_k: int = 5,
    ):
        print("Initializing Hybrid Retriever...")

        self.vector_k = vector_k
        self.graph_k = graph_k

        # -----------------------------
        # FAISS
        # -----------------------------

        print("Loading FAISS vector store...")

        self.vector_store = FAISSVectorStore()

        print("FAISS vector store ready.")

        # -----------------------------
        # Neo4j
        # -----------------------------

        print("Loading Neo4j graph retriever...")

        self.graph_retriever = GraphRetriever()

        print("Neo4j graph retriever ready.")

        print("\nHybrid Retriever ready.")

    # ==================================================
    # RETRIEVE
    # ==================================================

    def retrieve(
        self,
        question: str,
    ) -> Dict[str, Any]:

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        question = question.strip()

        print("\n" + "=" * 60)
        print("HYBRID RETRIEVAL")
        print("=" * 60)

        print(
            f"\nQuestion: {question}"
        )

        # ==================================================
        # FAISS
        # ==================================================

        print("\nSearching FAISS...")

        vector_results = (
            self.vector_store.search(
                question,
                k=self.vector_k,
            )
        )

        print(
            f"FAISS results: "
            f"{len(vector_results)}"
        )

        # ==================================================
        # NEO4J
        # ==================================================

        print("\nSearching Neo4j...")

        graph_results = (
            self.graph_retriever.retrieve(
                question,
                entity_limit=self.graph_k,
                relationship_limit=self.graph_k,
                chunk_limit=self.graph_k,
            )
        )

        graph_entities = (
            graph_results.get(
                "entities",
                [],
            )
        )

        graph_relationships = (
            graph_results.get(
                "relationships",
                [],
            )
        )

        graph_chunks = (
            graph_results.get(
                "chunks",
                [],
            )
        )

        print(
            "Neo4j entities:",
            len(graph_entities),
        )

        print(
            "Neo4j relationships:",
            len(graph_relationships),
        )

        print(
            "Neo4j chunks:",
            len(graph_chunks),
        )

        # ==================================================
        # MERGE
        # ==================================================

        merged_chunks = []

        # FAISS chunks

        for item in vector_results:

            chunk = dict(item)

            chunk[
                "retrieval_source"
            ] = "faiss"

            merged_chunks.append(
                chunk
            )

        # Neo4j chunks

        for item in graph_chunks:

            chunk = dict(item)

            chunk[
                "retrieval_source"
            ] = "neo4j"

            merged_chunks.append(
                chunk
            )

        # ==================================================
        # DEDUPLICATION
        # ==================================================

        unique = {}

        for chunk in merged_chunks:

            chunk_id = chunk.get(
                "chunk_id"
            )

            if not chunk_id:

                # Keep chunks without IDs
                key = (
                    f"anonymous_"
                    f"{len(unique)}"
                )

                unique[key] = chunk

                continue

            if chunk_id not in unique:

                unique[chunk_id] = chunk

            else:

                existing = unique[
                    chunk_id
                ]

                old_source = existing.get(
                    "retrieval_source",
                    "",
                )

                new_source = chunk.get(
                    "retrieval_source",
                    "",
                )

                sources = set()

                if old_source:
                    sources.update(
                        old_source.split(",")
                    )

                if new_source:
                    sources.add(
                        new_source
                    )

                existing[
                    "retrieval_source"
                ] = ",".join(
                    sorted(sources)
                )

        merged_chunks = list(
            unique.values()
        )

        print(
            "\nMerged unique chunks:",
            len(merged_chunks),
        )

        # ==================================================
        # RETURN CONTRACT
        # ==================================================

        return {

            "question": question,

            # FAISS
            "vector_results": vector_results,

            # Neo4j
            "graph_results": graph_results,

            "graph_entities": (
                graph_entities
            ),

            "graph_relationships": (
                graph_relationships
            ),

            "graph_chunks": (
                graph_chunks
            ),

            # IMPORTANT
            # Existing test expects this.
            "merged_chunks": (
                merged_chunks
            ),

            # Backward compatibility
            "combined_chunks": (
                merged_chunks
            ),
        }

    # ==================================================
    # CLOSE
    # ==================================================

    def close(self):

        try:

            if self.graph_retriever:

                self.graph_retriever.close()

        except Exception as exc:

            print(
                "Warning while closing "
                "Neo4j:",
                exc,
            )

        print(
            "Hybrid Retriever closed."
        )
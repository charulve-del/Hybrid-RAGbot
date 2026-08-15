from typing import Any, Dict, List

from src.vector_store.faiss_store import FAISSVectorStore
from src.retrieval.graph_retriever import GraphRetriever


class HybridRetriever:

    def __init__(
        self,
        vector_k: int = 5,
        graph_k: int = 5,
        graph_entity_limit: int | None = None,
        graph_relationship_limit: int = 10,
        graph_chunk_limit: int | None = None,
    ):
        """
        Hybrid FAISS + Neo4j retriever.

        graph_k is kept for backward compatibility with
        older test scripts.
        """

        self.vector_k = vector_k

        # Backward compatibility
        if graph_entity_limit is None:
            graph_entity_limit = graph_k

        if graph_chunk_limit is None:
            graph_chunk_limit = graph_k

        self.graph_entity_limit = graph_entity_limit
        self.graph_relationship_limit = (
            graph_relationship_limit
        )
        self.graph_chunk_limit = graph_chunk_limit

        print(
            "\nInitializing Hybrid Retriever..."
        )

        # --------------------------------------------------
        # FAISS
        # --------------------------------------------------

        print(
            "Creating FAISS vector store..."
        )

        self.vector_store = FAISSVectorStore()

        # --------------------------------------------------
        # Neo4j
        # --------------------------------------------------

        print(
            "Creating Graph Retriever..."
        )

        self.graph_retriever = GraphRetriever()

        print(
            "Hybrid Retriever ready."
        )

    # ======================================================
    # RETRIEVE
    # ======================================================

    def retrieve(
        self,
        question: str,
    ) -> Dict[str, Any]:

        question = question.strip()

        if not question:
            return {
                "question": question,
                "vector_results": [],
                "graph_entities": [],
                "graph_relationships": [],
                "graph_chunks": [],
                "merged_chunks": [],
            }

        print(
            "\n" + "=" * 60
        )
        print("HYBRID RETRIEVAL")
        print("=" * 60)

        print(
            f"\nQuestion: {question}"
        )

        # ==================================================
        # FAISS
        # ==================================================

        print(
            "\nSearching FAISS..."
        )

        vector_results = self.vector_store.search(
            question,
            k=self.vector_k,
        )

        print(
            f"FAISS results: {len(vector_results)}"
        )

        # ==================================================
        # NEO4J
        # ==================================================

        print(
            "\nSearching Neo4j..."
        )

        graph_results = self.graph_retriever.retrieve(
            question,
            entity_limit=self.graph_entity_limit,
            relationship_limit=(
                self.graph_relationship_limit
            ),
            chunk_limit=self.graph_chunk_limit,
        )

        graph_entities = graph_results.get(
            "entities",
            [],
        )

        graph_relationships = graph_results.get(
            "relationships",
            [],
        )

        graph_chunks = graph_results.get(
            "chunks",
            [],
        )

        print(
            f"Graph entities: {len(graph_entities)}"
        )

        print(
            f"Graph relationships: "
            f"{len(graph_relationships)}"
        )

        print(
            f"Graph chunks: {len(graph_chunks)}"
        )

        # ==================================================
        # MERGE
        # ==================================================

        merged_chunks = self._merge_chunks(
            vector_results,
            graph_chunks,
        )

        print(
            f"\nMerged chunks: {len(merged_chunks)}"
        )

        # ==================================================
        # RETURN
        # ==================================================

        return {
            "question": question,

            "vector_results": vector_results,

            "graph_entities": graph_entities,

            "graph_relationships": (
                graph_relationships
            ),

            "graph_chunks": graph_chunks,

            "merged_chunks": merged_chunks,
        }

    # ======================================================
    # MERGE CHUNKS
    # ======================================================

    @staticmethod
    def _merge_chunks(
        vector_results: List[Dict[str, Any]],
        graph_chunks: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        merged: Dict[str, Dict[str, Any]] = {}

        # --------------------------------------------------
        # FAISS results
        # --------------------------------------------------

        for item in vector_results:

            chunk_id = item.get("chunk_id")

            if not chunk_id:
                continue

            result = dict(item)

            result["retrieval_source"] = "vector"

            result["vector_score"] = item.get(
                "distance"
            )

            result["graph_match"] = False

            merged[chunk_id] = result

        # --------------------------------------------------
        # Neo4j results
        # --------------------------------------------------

        for item in graph_chunks:

            chunk_id = item.get("chunk_id")

            if not chunk_id:
                continue

            if chunk_id in merged:

                merged[chunk_id][
                    "retrieval_source"
                ] = "hybrid"

                merged[chunk_id][
                    "graph_match"
                ] = True

            else:

                result = dict(item)

                result["retrieval_source"] = "graph"

                result["graph_match"] = True

                merged[chunk_id] = result

        return list(
            merged.values()
        )

    # ======================================================
    # CLOSE
    # ======================================================

    def close(self):

        print(
            "\nClosing Hybrid Retriever..."
        )

        if self.graph_retriever:
            self.graph_retriever.close()

        print(
            "Hybrid Retriever closed."
        )
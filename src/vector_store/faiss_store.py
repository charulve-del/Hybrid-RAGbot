import json
from pathlib import Path
from typing import List, Dict, Any

import faiss
import numpy as np

from src.embeddings.openai_embeddings import (
    create_embeddings,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHUNKS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "chunks"
    / "chunks.json"
)

FAISS_DIR = (
    PROJECT_ROOT
    / "data"
    / "vector_store"
    / "faiss"
)

INDEX_FILE = FAISS_DIR / "index.faiss"
METADATA_FILE = FAISS_DIR / "metadata.json"


class FAISSVectorStore:

    def __init__(self):

        self.index = None
        self.metadata = []

    # --------------------------------------------------
    # Load chunks
    # --------------------------------------------------

    def load_chunks(self) -> List[Dict[str, Any]]:

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

    # --------------------------------------------------
    # Build index
    # --------------------------------------------------

    def build(self):

        print("\n" + "=" * 60)
        print("BUILDING FAISS VECTOR STORE")
        print("=" * 60)

        chunks = self.load_chunks()

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        print(
            f"\nTexts to embed: {len(texts)}"
        )

        print(
            "\nCreating embeddings..."
        )

        embeddings = create_embeddings(
            texts
        )

        print(
            "Embeddings created."
        )

        vectors = np.asarray(
            embeddings,
            dtype="float32",
        )

        print(
            "\nVector shape:",
            vectors.shape,
        )

        dimension = vectors.shape[1]

        print(
            f"Embedding dimension: {dimension}"
        )

        # ------------------------------------------
        # Create FAISS index
        # ------------------------------------------

        print(
            "\nCreating FAISS index..."
        )

        self.index = faiss.IndexFlatL2(
            dimension
        )

        print(
            "FAISS index created."
        )

        # ------------------------------------------
        # Add vectors
        # ------------------------------------------

        print(
            f"\nAdding {len(vectors)} vectors..."
        )

        self.index.add(vectors)

        print(
            "Vectors added:",
            self.index.ntotal,
        )

        # ------------------------------------------
        # Store metadata
        # ------------------------------------------

        self.metadata = []

        for chunk in chunks:

            self.metadata.append(
                {
                    "chunk_id": chunk[
                        "chunk_id"
                    ],
                    "document_id": chunk[
                        "document_id"
                    ],
                    "source": chunk[
                        "source"
                    ],
                    "file_path": chunk[
                        "file_path"
                    ],
                    "department": chunk[
                        "department"
                    ],
                    "document_type": chunk.get(
                        "document_type",
                        "unknown",
                    ),
                    "page_start": chunk[
                        "page_start"
                    ],
                    "page_end": chunk[
                        "page_end"
                    ],
                    "section": chunk.get(
                        "section"
                    ),
                    "title": chunk.get(
                        "title"
                    ),
                    "text": chunk[
                        "text"
                    ],
                }
            )

        # ------------------------------------------
        # Save
        # ------------------------------------------

        FAISS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        print(
            "\nSaving FAISS index..."
        )

        faiss.write_index(
            self.index,
            str(INDEX_FILE),
        )

        print(
            "Index saved:"
        )

        print(INDEX_FILE)

        print(
            "\nSaving metadata..."
        )

        with open(
            METADATA_FILE,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.metadata,
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(
            "Metadata saved:"
        )

        print(METADATA_FILE)

        print("\n" + "=" * 60)
        print("FAISS BUILD COMPLETE")
        print("=" * 60)

    # --------------------------------------------------
    # Load existing index
    # --------------------------------------------------

    def load(self):

        print(
            "\nLoading FAISS index..."
        )

        if not INDEX_FILE.exists():

            raise FileNotFoundError(
                f"FAISS index not found: "
                f"{INDEX_FILE}"
            )

        if not METADATA_FILE.exists():

            raise FileNotFoundError(
                f"Metadata not found: "
                f"{METADATA_FILE}"
            )

        self.index = faiss.read_index(
            str(INDEX_FILE)
        )

        with open(
            METADATA_FILE,
            "r",
            encoding="utf-8",
        ) as f:

            self.metadata = json.load(f)

        print(
            "FAISS index loaded."
        )

        print(
            "Vectors:",
            self.index.ntotal,
        )

        print(
            "Metadata records:",
            len(self.metadata),
        )

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search(
        self,
        query: str,
        k: int = 5,
    ) -> List[Dict[str, Any]]:

        if self.index is None:

            self.load()

        print(
            f"\nEmbedding query: {query}"
        )

        query_embedding = create_embeddings(
            [query]
        )

        query_vector = np.asarray(
            query_embedding,
            dtype="float32",
        )

        distances, indices = (
            self.index.search(
                query_vector,
                k,
            )
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0],
        ):

            if index < 0:
                continue

            metadata = dict(
                self.metadata[index]
            )

            metadata[
                "distance"
            ] = float(distance)

            metadata[
                "retrieval_source"
            ] = "vector"

            results.append(
                metadata
            )

        return results
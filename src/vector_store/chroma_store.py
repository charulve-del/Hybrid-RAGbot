import json
from typing import List

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from src.config import (
    CHUNKS_FILE,
    CHROMA_DIR,
    CHROMA_COLLECTION_NAME,
    OPENAI_API_KEY,
)


EMBEDDING_MODEL = "text-embedding-3-small"
BATCH_SIZE = 20


def load_chunks() -> list:

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_FILE}"
        )

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        chunks = json.load(f)

    if not isinstance(chunks, list):
        raise ValueError(
            "chunks.json must contain a JSON list."
        )

    return chunks


def chunk_to_document(chunk: dict) -> Document:

    metadata = {
        "chunk_id": chunk["chunk_id"],
        "document_id": chunk["document_id"],
        "source": chunk["source"],
        "file_path": chunk["file_path"],
        "department": chunk["department"],
        "document_type": chunk["document_type"],
        "page_start": chunk["page_start"],
        "page_end": chunk["page_end"],
        "chunk_index": chunk["chunk_index"],
    }

    optional_fields = [
        "section",
        "title",
        "version",
        "effective_date",
        "supersedes_document_id",
    ]

    for field in optional_fields:

        value = chunk.get(field)

        if value is not None:
            metadata[field] = value

    return Document(
        page_content=chunk["text"],
        metadata=metadata,
    )


def create_vector_store() -> Chroma:

    print("\nLoading chunks...")

    chunks = load_chunks()

    print(
        f"Loaded chunks: {len(chunks)}"
    )

    documents: List[Document] = [
        chunk_to_document(chunk)
        for chunk in chunks
    ]

    print(
        f"Converted to LangChain documents: "
        f"{len(documents)}"
    )

    print("\nCreating OpenAI embeddings client...")

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY,
    )

    print("Embeddings client ready.")

    CHROMA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("\nCreating Chroma...")

    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    print("Chroma ready.")

    total = len(documents)

    print(
        f"\nAdding {total} documents "
        f"in batches of {BATCH_SIZE}..."
    )

    for start in range(
        0,
        total,
        BATCH_SIZE,
    ):

        end = min(
            start + BATCH_SIZE,
            total,
        )

        batch_documents = documents[start:end]

        batch_ids = [
            chunks[i]["chunk_id"]
            for i in range(start, end)
        ]

        print(
            f"\nEmbedding/adding "
            f"{start + 1}-{end} "
            f"of {total}..."
        )

        try:

            vector_store.add_documents(
                documents=batch_documents,
                ids=batch_ids,
            )

            print(
                f"SUCCESS: {end}/{total}"
            )

        except Exception as e:

            print(
                f"\nERROR in batch "
                f"{start + 1}-{end}"
            )

            print(
                "Exception type:",
                type(e).__name__,
            )

            print(
                "Exception:",
                str(e),
            )

            raise

    print(
        f"\nSuccessfully indexed "
        f"{total} documents."
    )

    return vector_store
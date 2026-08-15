import json

import chromadb

from src.config import (
    CHROMA_DIR,
    CHROMA_COLLECTION_NAME,
    CHUNKS_FILE,
)


def main():

    print("=" * 60)
    print("DIRECT CHROMA INSERT TEST")
    print("=" * 60)

    # --------------------------------------------------
    # Load chunks
    # --------------------------------------------------

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

    # Only test first 20
    chunks = chunks[:20]

    print(
        f"Testing with {len(chunks)} chunks."
    )

    # --------------------------------------------------
    # Create embeddings
    # --------------------------------------------------

    print("\nCreating embeddings...")

    from langchain_openai import OpenAIEmbeddings
    from src.config import OPENAI_API_KEY

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=OPENAI_API_KEY,
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    vectors = embeddings.embed_documents(
        texts
    )

    print(
        f"Created {len(vectors)} embeddings."
    )

    # --------------------------------------------------
    # Create Chroma client
    # --------------------------------------------------

    print("\nCreating Chroma client...")

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    print("Chroma client created.")

    # --------------------------------------------------
    # Create collection
    # --------------------------------------------------

    print(
        "\nCreating/getting collection..."
    )

    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME
    )

    print("Collection ready.")

    # --------------------------------------------------
    # Prepare data
    # --------------------------------------------------

    ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = []

    for chunk in chunks:

        metadata = {
            "document_id": chunk["document_id"],
            "source": chunk["source"],
            "file_path": chunk["file_path"],
            "department": chunk["department"],
            "document_type": chunk["document_type"],
            "page_start": chunk["page_start"],
            "page_end": chunk["page_end"],
            "chunk_index": chunk["chunk_index"],
        }

        metadatas.append(metadata)

    # --------------------------------------------------
    # Insert
    # --------------------------------------------------

    print(
        "\nInserting 20 records into Chroma..."
    )

    try:

        collection.add(
            ids=ids,
            embeddings=vectors,
            documents=documents,
            metadatas=metadatas,
        )

        print(
            "\nSUCCESS!"
        )

    except Exception as e:

        print(
            "\nCHROMA INSERT ERROR"
        )

        print(
            "Exception type:",
            type(e).__name__,
        )

        print(
            "Exception:",
            str(e),
        )

        import traceback

        traceback.print_exc()

        return

    # --------------------------------------------------
    # Verify
    # --------------------------------------------------

    print(
        "\nChecking inserted records..."
    )

    result = collection.get(
        limit=20
    )

    print(
        "Records returned:",
        len(result["ids"]),
    )

    print("\nSample IDs:")

    for chunk_id in result["ids"][:5]:

        print(
            " ",
            chunk_id,
        )

    print("\n" + "=" * 60)
    print("DIRECT CHROMA TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
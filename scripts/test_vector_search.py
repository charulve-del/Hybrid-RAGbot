from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from src.config import (
    CHROMA_DIR,
    CHROMA_COLLECTION_NAME,
)


EMBEDDING_MODEL = "text-embedding-3-small"


def main():

    print("=" * 60)
    print("VECTOR SEARCH TEST")
    print("=" * 60)

    print("\nLoading embeddings...")

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )

    print("Embeddings ready.")

    print("\nOpening Chroma...")

    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    print("Chroma ready.")

    query = input(
        "\nEnter your policy question: "
    ).strip()

    if not query:
        print("No question entered.")
        return

    print(
        f"\nSearching for: {query}"
    )

    print("Calling similarity search...")

    results = vector_store.similarity_search(
        query,
        k=5,
    )

    print(
        f"\nNumber of results: {len(results)}"
    )

    if len(results) == 0:
        print("No results found.")
        return

    print("\n" + "=" * 60)
    print("TOP RESULTS")
    print("=" * 60)

    for i, doc in enumerate(
        results,
        start=1,
    ):

        print(f"\nRESULT {i}")
        print("-" * 60)

        print(
            "Chunk ID:",
            doc.metadata.get("chunk_id"),
        )

        print(
            "Source:",
            doc.metadata.get("source"),
        )

        print(
            "Document:",
            doc.metadata.get("document_id"),
        )

        print(
            "Department:",
            doc.metadata.get("department"),
        )

        print(
            "Page:",
            doc.metadata.get("page_start"),
        )

        print(
            "Section:",
            doc.metadata.get("section"),
        )

        print("\nTEXT:")
        print(doc.page_content)

    print("\n" + "=" * 60)
    print("VECTOR SEARCH COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
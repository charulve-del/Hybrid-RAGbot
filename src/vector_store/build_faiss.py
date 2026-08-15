from src.vector_store.faiss_store import (
    FAISSVectorStore,
)


def main():

    store = FAISSVectorStore()

    store.build()


if __name__ == "__main__":
    main()
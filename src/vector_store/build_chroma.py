import shutil

from src.config import CHROMA_DIR
from src.vector_store.chroma_store import (
    create_vector_store,
)


def main():

    print("=" * 60)
    print("BUILDING CHROMA VECTOR STORE")
    print("=" * 60)

    if CHROMA_DIR.exists():
        print(
            f"Removing existing Chroma DB: "
            f"{CHROMA_DIR}"
        )

        shutil.rmtree(CHROMA_DIR)

    create_vector_store()

    print("=" * 60)
    print("CHROMA BUILD COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
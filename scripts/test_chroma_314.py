import chromadb
import numpy as np

from src.config import CHROMA_DIR


def test_insert(collection, vector, name):

    print(f"\n--- Testing {name} ---")
    print("Vector type:", type(vector))
    print("Vector length:", len(vector))

    try:

        collection.add(
            ids=[f"test-{name}"],
            embeddings=[vector],
            documents=[
                f"Chroma test using {name}"
            ],
            metadatas=[
                {"test": name}
            ],
        )

        print("INSERT SUCCESS")

    except Exception as e:

        print("INSERT FAILED")
        print("Type:", type(e).__name__)
        print("Error:", str(e))

        import traceback
        traceback.print_exc()


def main():

    print("=" * 60)
    print("CHROMA PYTHON 3.14 TEST")
    print("=" * 60)

    print("\nPython/Chroma:")
    print(chromadb.__version__)

    print("\nCreating PersistentClient...")

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    print("Client created.")

    collection = client.get_or_create_collection(
        name="python314_test"
    )

    print("Collection created.")

    # -----------------------------------------
    # Test 1: normal Python list
    # -----------------------------------------

    vector_list = [
        0.1,
        0.2,
        0.3,
        0.4,
    ]

    test_insert(
        collection,
        vector_list,
        "python_list",
    )

    # -----------------------------------------
    # Test 2: NumPy float32
    # -----------------------------------------

    vector_numpy = np.array(
        [0.1, 0.2, 0.3, 0.4],
        dtype=np.float32,
    )

    test_insert(
        collection,
        vector_numpy.tolist(),
        "numpy_float32",
    )

    # -----------------------------------------
    # Read
    # -----------------------------------------

    print("\nReading collection...")

    try:

        result = collection.get()

        print(
            "Records:",
            len(result["ids"]),
        )

        print(
            "IDs:",
            result["ids"],
        )

    except Exception as e:

        print(
            "READ FAILED:",
            type(e).__name__,
            str(e),
        )

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
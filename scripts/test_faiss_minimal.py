import faiss
import numpy as np


def main():

    print("=" * 60)
    print("FAISS MINIMAL TEST")
    print("=" * 60)

    print(
        "\nFAISS version:",
        faiss.__version__,
    )

    # ------------------------------------------
    # Create 4-dimensional vectors
    # ------------------------------------------

    vectors = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ],
        dtype="float32",
    )

    print(
        "\nVector shape:",
        vectors.shape,
    )

    # ------------------------------------------
    # Create FAISS index
    # ------------------------------------------

    dimension = vectors.shape[1]

    print(
        "\nCreating FAISS index..."
    )

    index = faiss.IndexFlatL2(
        dimension
    )

    print(
        "Index created."
    )

    # ------------------------------------------
    # Add vectors
    # ------------------------------------------

    print(
        "\nAdding vectors..."
    )

    index.add(vectors)

    print(
        "Vectors added:",
        index.ntotal,
    )

    # ------------------------------------------
    # Search
    # ------------------------------------------

    query = np.array(
        [
            [1.0, 0.0, 0.0, 0.0]
        ],
        dtype="float32",
    )

    print(
        "\nSearching..."
    )

    distances, indices = index.search(
        query,
        2,
    )

    print(
        "Distances:",
        distances,
    )

    print(
        "Indices:",
        indices,
    )

    print("\n" + "=" * 60)
    print("FAISS TEST SUCCESSFUL")
    print("=" * 60)


if __name__ == "__main__":
    main()
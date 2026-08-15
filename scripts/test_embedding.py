from langchain_openai import OpenAIEmbeddings

from src.config import OPENAI_API_KEY


def main():

    print("=" * 60)
    print("OPENAI EMBEDDING TEST")
    print("=" * 60)

    try:

        print(
            "\nAPI key loaded:",
            bool(OPENAI_API_KEY),
        )

        print(
            "API key length:",
            len(OPENAI_API_KEY)
            if OPENAI_API_KEY
            else 0,
        )

        print("\nCreating embedding client...")

        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=OPENAI_API_KEY,
        )

        print("Client created.")

        text = (
            "What is the laptop request process?"
        )

        print("\nRequesting embedding...")

        vector = embeddings.embed_query(text)

        print("\nEmbedding received.")

        print(
            "Vector type:",
            type(vector),
        )

        print(
            "Vector length:",
            len(vector),
        )

        print("\nFirst 5 values:")
        print(vector[:5])

        print("\n" + "=" * 60)
        print("SUCCESS")
        print("=" * 60)

    except Exception as e:

        print("\n" + "=" * 60)
        print("ERROR")
        print("=" * 60)

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

        print("=" * 60)


if __name__ == "__main__":
    main()
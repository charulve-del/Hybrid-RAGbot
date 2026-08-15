from openai import OpenAI

from src.config import OPENAI_API_KEY


def main():

    print("=" * 60)
    print("OPENAI CONNECTION TEST")
    print("=" * 60)

    print("\nAPI key loaded:", bool(OPENAI_API_KEY))

    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY is missing.")
        return

    print("Creating OpenAI client...")

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    print("OpenAI client created.")

    print("\nSending test request...")

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="What is the laptop request process?",
    )

    print("Response received.")

    vector = response.data[0].embedding

    print("Vector type:", type(vector))
    print("Vector length:", len(vector))

    print("\nFirst 5 values:")
    print(vector[:5])

    print("\n" + "=" * 60)
    print("OPENAI CONNECTION TEST SUCCESS")
    print("=" * 60)


if __name__ == "__main__":
    main()
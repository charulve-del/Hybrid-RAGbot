import json
from pathlib import Path


CHUNKS_FILE = Path("data/processed/chunks/chunks.json")


def main():
    if not CHUNKS_FILE.exists():
        print(f"ERROR: File not found: {CHUNKS_FILE}")
        return

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print("=" * 60)
    print("CHUNK VALIDATION")
    print("=" * 60)

    print(f"Python type: {type(chunks).__name__}")

    if not isinstance(chunks, list):
        print("ERROR: chunks.json must contain a JSON list.")
        return

    print(f"Total chunks: {len(chunks)}")

    if len(chunks) == 0:
        print("ERROR: No chunks found.")
        return

    required_fields = [
        "chunk_id",
        "document_id",
        "source",
        "file_path",
        "department",
        "document_type",
        "text",
        "page_start",
        "page_end",
        "chunk_index",
    ]

    optional_fields = [
        "section",
        "title",
        "version",
        "effective_date",
        "supersedes_document_id",
    ]

    errors = 0

    for i, chunk in enumerate(chunks):

        if not isinstance(chunk, dict):
            print(f"ERROR: Chunk {i} is not an object.")
            errors += 1
            continue

        # Check required fields
        for field in required_fields:
            if field not in chunk:
                print(
                    f"ERROR: Chunk {i} missing field: {field}"
                )
                errors += 1

        # Validate text
        if "text" in chunk:

            if not isinstance(chunk["text"], str):
                print(
                    f"ERROR: Chunk {i} text is not a string."
                )
                errors += 1

            elif not chunk["text"].strip():
                print(
                    f"ERROR: Chunk {i} has empty text."
                )
                errors += 1

        # Validate chunk index
        if "chunk_index" in chunk:

            if not isinstance(chunk["chunk_index"], int):
                print(
                    f"ERROR: Chunk {i} chunk_index "
                    f"is not an integer."
                )
                errors += 1

            elif chunk["chunk_index"] < 0:
                print(
                    f"ERROR: Chunk {i} chunk_index "
                    f"is negative."
                )
                errors += 1

        # Validate page numbers
        if "page_start" in chunk:
            if not isinstance(chunk["page_start"], int):
                print(
                    f"ERROR: Chunk {i} page_start "
                    f"is not an integer."
                )
                errors += 1

        if "page_end" in chunk:
            if not isinstance(chunk["page_end"], int):
                print(
                    f"ERROR: Chunk {i} page_end "
                    f"is not an integer."
                )
                errors += 1

    print("-" * 60)

    if errors == 0:
        print("SUCCESS: All chunks are structurally valid.")
    else:
        print(f"FAILED: {errors} validation errors.")

    print("=" * 60)


if __name__ == "__main__":
    main()
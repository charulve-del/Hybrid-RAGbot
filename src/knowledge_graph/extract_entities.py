import json
import time
from pathlib import Path

from openai import OpenAI

from src.config import (
    OPENAI_API_KEY,
    CHUNKS_FILE,
)

from src.knowledge_graph.extraction_schema import (
    KnowledgeGraphExtraction,
)


MODEL = "gpt-4.1-mini"

BATCH_SIZE = 10

OUTPUT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "knowledge_graph"
    / "extractions.json"
)


SYSTEM_PROMPT = """
You extract knowledge graph information from company policy documents.

Extract only information explicitly supported by the supplied text.

Allowed entity types:

- Policy
- Process
- Role
- Department
- System
- Equipment
- Approval
- Document

Allowed relationship types:

- REQUIRES_APPROVAL
- PERFORMED_BY
- OWNED_BY
- USES
- INVOLVES
- DESCRIBES
- CONTAINS

Rules:

1. Do not invent entities.
2. Do not infer relationships that are not supported by the text.
3. Keep entity names concise.
4. Use terminology from the policy whenever possible.
5. Only extract relationships supported by the text.
6. If there are no useful entities or relationships, return empty lists.
"""


def extract_chunk(client, chunk):

    response = client.responses.parse(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    "Extract knowledge graph "
                    "information from this policy chunk.\n\n"
                    f"Document: {chunk['document_id']}\n"
                    f"Page: {chunk['page_start']}\n\n"
                    f"{chunk['text']}"
                ),
            },
        ],
        text_format=KnowledgeGraphExtraction,
    )

    extraction = response.output_parsed

    return {
        "chunk_id": chunk["chunk_id"],
        "document_id": chunk["document_id"],
        "source": chunk["source"],
        "file_path": chunk["file_path"],
        "department": chunk["department"],
        "document_type": chunk.get(
            "document_type",
            "unknown",
        ),
        "page_start": chunk["page_start"],
        "page_end": chunk["page_end"],
        "extraction": extraction.model_dump(),
    }


def main():

    print("=" * 60)
    print("BUILDING KNOWLEDGE GRAPH EXTRACTIONS")
    print("=" * 60)

    print("\nLoading chunks...")

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        chunks = json.load(f)

    print(
        f"Total chunks: {len(chunks)}"
    )

    print(
        "\nCreating OpenAI client..."
    )

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    print(
        "OpenAI client ready."
    )

    results = []

    total = len(chunks)

    for start in range(
        0,
        total,
        BATCH_SIZE,
    ):

        end = min(
            start + BATCH_SIZE,
            total,
        )

        batch = chunks[start:end]

        print(
            f"\nProcessing chunks "
            f"{start + 1}-{end} "
            f"of {total}..."
        )

        for chunk in batch:

            try:

                result = extract_chunk(
                    client,
                    chunk,
                )

                results.append(result)

                entity_count = len(
                    result["extraction"][
                        "entities"
                    ]
                )

                relationship_count = len(
                    result["extraction"][
                        "relationships"
                    ]
                )

                print(
                    f"  {chunk['chunk_id']} "
                    f"-> "
                    f"{entity_count} entities, "
                    f"{relationship_count} relationships"
                )

            except Exception as e:

                print(
                    f"  ERROR: "
                    f"{chunk['chunk_id']}"
                )

                print(
                    f"  {type(e).__name__}: {e}"
                )

        # Small pause between batches
        time.sleep(1)

        # Save progress after every batch
        OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                results,
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(
            f"Progress saved: "
            f"{len(results)}/{total}"
        )

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)

    print(
        f"\nChunks processed: {len(results)}"
    )

    print(
        f"Output file:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
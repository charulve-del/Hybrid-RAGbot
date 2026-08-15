from typing import Dict, Any, List

from src.ingestion.metadata import DocumentChunk


def chunk_document(
    document: Dict[str, Any],
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> List[DocumentChunk]:

    chunks = []

    for page in document["pages"]:
        text = page["text"]

        if not text:
            continue

        page_number = page["page_number"]

        start = 0
        chunk_index = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunk = DocumentChunk(
                    chunk_id=(
                        f"{document['document_id']}"
                        f"_p{page_number}"
                        f"_c{chunk_index}"
                    ),
                    document_id=document["document_id"],
                    source=document["source"],
                    file_path=document["file_path"],
                    department=document["department"],
                    document_type=document.get(
                        "document_type",
                        "unknown",
                    ),
                    text=chunk_text,
                    page_start=page_number,
                    page_end=page_number,
                    chunk_index=chunk_index,
                )

                chunks.append(chunk)

            start = end - chunk_overlap
            chunk_index += 1

    return chunks
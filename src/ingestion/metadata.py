from typing import Optional

from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """
    Canonical representation of a chunk.

    This object will eventually be used by:
    1. Vector database
    2. Knowledge graph
    3. Retrieval
    4. Citation generation
    """

    # Identity
    chunk_id: str
    document_id: str

    # Source information
    source: str
    file_path: str

    # Organization
    department: str
    document_type: str = "unknown"

    # Content
    text: str

    # Location / citation
    page_start: int
    page_end: int
    section: Optional[str] = None

    # Policy information
    title: Optional[str] = None
    version: Optional[str] = None
    effective_date: Optional[str] = None

    # Relationships
    supersedes_document_id: Optional[str] = None

    # Retrieval metadata
    chunk_index: int = Field(ge=0)
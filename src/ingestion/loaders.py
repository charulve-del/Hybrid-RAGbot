from pathlib import Path
from typing import List, Dict, Any

from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf"}


def detect_department(file_path: Path) -> str:
    """
    Infer department from the directory structure.

    Example:
        data/raw/hr/leave_policy.pdf
        -> hr
    """
    department = file_path.parent.name.lower()

    allowed_departments = {
        "hr",
        "finance",
        "it",
        "operations",
    }

    if department in allowed_departments:
        return department

    return "unknown"


def load_pdf(file_path: Path) -> Dict[str, Any]:
    """
    Load a single PDF while preserving page boundaries.
    """

    reader = PdfReader(str(file_path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append(
            {
                "page_number": page_number,
                "text": text.strip(),
            }
        )

    return {
        "document_id": file_path.stem,
        "source": file_path.name,
        "file_path": str(file_path),
        "department": detect_department(file_path),
        "file_type": file_path.suffix.lower(),
        "page_count": len(pages),
        "pages": pages,
    }


def load_documents(data_dir: str = "data/raw") -> List[Dict[str, Any]]:
    """
    Recursively load all supported documents.
    """

    root = Path(data_dir)

    if not root.exists():
        raise FileNotFoundError(
            f"Data directory does not exist: {root}"
        )

    documents = []

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        print(f"Loading: {file_path}")

        document = load_pdf(file_path)
        documents.append(document)

    return documents
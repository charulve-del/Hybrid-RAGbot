from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEO4J_URI = os.getenv(
    "NEO4J_URI",
)

NEO4J_USERNAME = os.getenv(
    "NEO4J_USERNAME",
)

NEO4J_PASSWORD = os.getenv(
    "NEO4J_PASSWORD",
)

CHUNKS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "chunks"
    / "chunks.json"
)

CHROMA_DIR = (
    BASE_DIR
    / "data"
    / "vector_store"
    / "chroma"
)

CHROMA_COLLECTION_NAME = "company_policy_chunks"


if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is not set. "
        "Check your .env file."
    )
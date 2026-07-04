from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


# ===========================
# GROK
# ===========================

GROK_API_KEY = os.getenv("GROK_API_KEY")

GROK_MODEL = os.getenv(
    "GROK_MODEL",
    "grok-3-mini",
)


# ===========================
# CHROMADB
# ===========================

CHROMA_DB_PATH = os.getenv(
    "CHROMA_DB_PATH",
    "./memory/chroma_db",
)

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "research_memory",
)


# ===========================
# ITERATIONS
# ===========================

MAX_ITERATIONS = int(
    os.getenv("MAX_ITERATIONS", 3)
)

RQS_THRESHOLD = float(
    os.getenv("RQS_THRESHOLD", 8.5)
)
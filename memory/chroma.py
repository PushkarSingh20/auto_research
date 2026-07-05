"""
ChromaDB Memory

Persistent semantic memory for the research system.
"""

from __future__ import annotations

import logging
from uuid import uuid4
from typing import Any

import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
)

logger = logging.getLogger(__name__)


class ChromaMemory:
    """
    Wrapper around ChromaDB.

    Handles:
    - Collection creation
    - Document storage
    - Semantic retrieval
    """

    def __init__(self) -> None:
        self.client: chromadb.PersistentClient | None = None
        self.collection: Any | None = None
        self.disabled = False

    def _get_collection(self) -> Any:
        """
        Lazily initialize ChromaDB and the sentence-transformer embedding model.

        This keeps the application importable in environments where the local
        embedding model has not been downloaded yet. Memory operations still use
        ChromaDB + Sentence Transformers when the model is available.
        """

        if self.collection is not None:
            return self.collection

        if self.disabled:
            raise RuntimeError("Chroma memory is unavailable in this environment.")

        try:
            self.client = chromadb.PersistentClient(
                path=CHROMA_DB_PATH,
            )

            embedding_function = SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2",
            )

            self.collection = self.client.get_or_create_collection(
                name=COLLECTION_NAME,
                embedding_function=embedding_function,
            )
        except Exception as exc:
            self.disabled = True
            raise RuntimeError("Unable to initialize Chroma memory.") from exc

        return self.collection

    # ---------------------------------------------------------

    def is_available(self) -> bool:
        """
        Check whether the Chroma memory backend is ready.
        """

        try:
            self._get_collection()
            return True
        except Exception:
            logger.warning("Chroma memory is not available.")
            return False

    # ---------------------------------------------------------

    def store_documents(
        self,
        query: str,
        documents: list[dict],
    ) -> None:
        """
        Store scraped documents.
        """

        if not documents:
            return

        try:
            collection = self._get_collection()
        except Exception:
            logger.warning("Skipping memory storage because Chroma is unavailable.")
            return

        ids = []
        texts = []
        metadatas = []

        for doc in documents:

            ids.append(str(uuid4()))

            texts.append(doc["content"])

            metadatas.append(
                {
                    "query": query,
                    "title": doc["title"],
                    "url": doc["url"],
                    "source_type": doc.get(
                        "source_type",
                        "web",
                    ),
                }
            )

        collection.add(

            ids=ids,
            documents=texts,
            metadatas=metadatas,

        )

        logger.info(
            "Stored %d documents.",
            len(documents),
        )

    # ---------------------------------------------------------

    def retrieve_documents(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Retrieve the most relevant documents.
        """

        try:
            collection = self._get_collection()
        except Exception:
            logger.warning("Skipping memory retrieval because Chroma is unavailable.")
            return []

        results = collection.query(

            query_texts=[query],
            n_results=top_k,

        )

        retrieved = []

        documents = results.get("documents", [[]])[0]

        metadatas = results.get("metadatas", [[]])[0]

        for doc, meta in zip(
            documents,
            metadatas,
        ):

            retrieved.append(

                {
                    "content": doc,
                    "metadata": meta,
                }

            )

        logger.info(
            "Retrieved %d documents.",
            len(retrieved),
        )

        return retrieved

    # ---------------------------------------------------------

    def count(self) -> int:
        """
        Return total stored documents.
        """

        if self.collection is None:
            try:
                client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
                collection = client.get_or_create_collection(name=COLLECTION_NAME)
                return collection.count()
            except Exception:
                logger.warning("Unable to count Chroma documents.")
                return 0

        try:
            return self.collection.count()
        except Exception:
            logger.warning("Unable to count Chroma documents.")
            return 0


memory = ChromaMemory()

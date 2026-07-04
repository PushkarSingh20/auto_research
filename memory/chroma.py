"""
ChromaDB Memory

Persistent semantic memory for the research system.
"""

from __future__ import annotations

import logging
from uuid import uuid4

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

        self.collection.add(

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

        results = self.collection.query(

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

        return self.collection.count()


memory = ChromaMemory()
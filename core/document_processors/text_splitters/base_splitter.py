from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from langchain_core.documents import Document


class BaseTextSplitter(ABC):
    """Abstract base class for all text splitters."""

    @abstractmethod
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.

        Args:
            documents: List of documents to split.

        Returns:
            List[Document]: List of split documents.
        """
        pass

    @abstractmethod
    def split_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Split text into chunks and create documents.

        Args:
            text: Text to split.
            metadata: Optional metadata to attach to the created documents.

        Returns:
            List[Document]: List of documents created from the text chunks.
        """
        pass
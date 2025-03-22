from typing import List, Optional, Dict, Any, Sequence

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter as LangchainRecursiveTextSplitter

from .base_splitter import BaseTextSplitter
from ....config.app_config import config


class RecursiveTextSplitter(BaseTextSplitter):
    """Wrapper for Langchain's RecursiveCharacterTextSplitter."""

    def __init__(
            self,
            chunk_size: int = None,
            chunk_overlap: int = None,
            separators: Optional[Sequence[str]] = None,
            keep_separator: bool = True,
            is_separator_regex: bool = False
    ):
        """
        Initialize the recursive text splitter.

        Args:
            chunk_size: Maximum size of chunks to return.
            chunk_overlap: Overlap in characters between chunks.
            separators: List of separators to use for splitting.
            keep_separator: Whether to keep the separator in the chunks.
            is_separator_regex: Whether the separators are regex patterns.
        """
        self.chunk_size = chunk_size or config.default_chunk_size
        self.chunk_overlap = chunk_overlap or config.default_chunk_overlap

        # Default separators in priority order if not provided
        default_separators = [
            "\n\n",  # Paragraphs
            "\n",  # Lines
            ". ",  # Sentences
            ", ",  # Phrases
            " ",  # Words
            ""  # Characters
        ]

        self.separators = separators or default_separators
        self.keep_separator = keep_separator
        self.is_separator_regex = is_separator_regex

        self._splitter = LangchainRecursiveTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            keep_separator=self.keep_separator,
            is_separator_regex=self.is_separator_regex
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks using recursive splitting.

        Args:
            documents: List of documents to split.

        Returns:
            List[Document]: List of split documents.
        """
        return self._splitter.split_documents(documents)

    def split_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Split text into chunks and create documents.

        Args:
            text: Text to split.
            metadata: Optional metadata to attach to the created documents.

        Returns:
            List[Document]: List of documents created from the text chunks.
        """
        metadata = metadata or {}
        return self._splitter.create_documents([text], [metadata])
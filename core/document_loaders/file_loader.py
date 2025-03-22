from pathlib import Path
from typing import List, Union, Dict, Any, Optional
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader

from .base_loader import BaseDocumentLoader


class SingleFileLoader(BaseDocumentLoader):
    """Loader for loading content from a single file."""

    def __init__(
            self,
            file_path: Union[str, Path],
            metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a single file loader.

        Args:
            file_path: Path to the file to load.
            metadata: Optional metadata to attach to the loaded document.
        """
        self.file_path = self._validate_path(file_path)
        self.metadata = metadata or {}

    @staticmethod
    def update_metadata(documents: List[Document], metadata: Dict[str, Any]) -> List[Document]:
        for doc in documents:
            doc.metadata.update(metadata)

        return documents

    def load(self) -> List[Document]:
        """
        Load document from the file based on its extension.

        Returns:
            List[Document]: A list containing the loaded document.

        Raises:
            ValueError: If file type is not supported.
        """
        extension = self._get_file_extension(self.file_path)

        # Create base metadata
        metadata = {
            "source": str(self.file_path),
            "file_path": str(self.file_path),
            "file_name": self.file_path.name,
            "file_type": extension,
            **self.metadata
        }

        # Load content based on file type
        if extension == "txt":
            return self._load_text_file(metadata)
        elif extension == "pdf":
            return self._load_pdf_file(metadata)
        elif extension == "csv":
            return self._load_csv_file(metadata)
        else:
            raise ValueError(f"Unsupported file type: {extension}")

    def _load_text_file(self, metadata: Dict[str, Any]) -> List[Document]:
        """Load content from a text file."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        return [Document(page_content=content, metadata=metadata)]

    def _load_pdf_file(self, metadata: Dict[str, Any]) -> List[Document]:
        """Load content from a PDF file."""
        try:
            import pypdf
        except ImportError:
            raise ImportError(
                "Could not import pypdf. Please install it with `pip install pypdf`."
            )

        loader = PyPDFLoader(self.file_path)
        documents = loader.load()
        documents = self.update_metadata(documents, metadata)
        return documents

    def _load_csv_file(self, metadata: Dict[str, Any]) -> List[Document]:
        loader = CSVLoader(file_path=self.file_path)
        documents = loader.load()
        documents = self.update_metadata(documents, metadata)
        return documents

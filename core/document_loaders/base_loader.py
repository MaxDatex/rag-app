from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union
from langchain_core.documents import Document


class BaseDocumentLoader(ABC):
    """Abstract base class for all document loaders."""

    @abstractmethod
    def load(self) -> List[Document]:
        """
        Load documents from the source.

        Returns:
            List[Document]: A list of loaded documents.
        """
        pass

    @staticmethod
    def _validate_path(path: Union[str, Path]) -> Path:
        """
        Validate if the given path exists.

        Args:
            path: Path to validate.

        Returns:
            Path: The validated Path object.

        Raises:
            FileNotFoundError: If path doesn't exist.
        """
        path_obj = Path(path) if isinstance(path, str) else path

        if not path_obj.exists():
            raise FileNotFoundError(f"Path does not exist: {path_obj}")

        return path_obj

    @staticmethod
    def _get_file_extension(file_path: Path) -> str:
        """
        Get the lowercase extension of a file without the dot.

        Args:
            file_path: Path to the file.

        Returns:
            str: Lowercase extension without dot.
        """
        return file_path.suffix.lower()[1:] if file_path.suffix else ""
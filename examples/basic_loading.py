import sys
from pathlib import Path
from loguru import logger


# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.document_loaders.file_loader import SingleFileLoader


def main():
    """Basic test of file loading functionality."""
    # Get a file path from command line or use a default
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        logger.debug("Please provide a file path as an argument.")
        logger.debug("Example: python examples/basic_loading.py path/to/document.pdf")
        return

    # Load the document
    try:
        loader = SingleFileLoader(file_path)
        documents = loader.load()

        logger.debug(f"Successfully loaded {len(documents)} document(s):")
        for i, doc in enumerate(documents):
            logger.debug(f"\nDocument {i + 1}:")
            logger.debug(f"  Source: {doc.metadata.get('source')}")
            logger.debug(f"  Type: {doc.metadata.get('file_type')}")
            logger.debug(f"  Content length: {len(doc.page_content)} characters")
            logger.debug(f"  Preview: {doc.page_content[:150]}...")

    except Exception as e:
        logger.error(f"Error loading document: {e}")


if __name__ == "__main__":
    main()
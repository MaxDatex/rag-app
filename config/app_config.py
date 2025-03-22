import os
from pathlib import Path
from pydantic import BaseModel
from typing import Literal, Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


class AppConfig(BaseModel):
    """Central configuration for the RAG application."""

    # Base paths
    base_dir: Path = Path(__file__).parent.parent
    data_dir: Path = Path(os.getenv("RAG_DATA_DIR", base_dir / "data"))

    # Vector store settings
    vector_store_type: Literal["chroma", "elasticsearch", "postgresql"] = os.getenv("VECTOR_STORE_TYPE", "chroma")

    # Vector store connection settings
    vector_store_config: Dict[str, Dict[str, Any]] = {
        "chroma": {
            "persist_directory": str(data_dir / "chroma_db"),
        },
        "elasticsearch": {
            "hosts": os.getenv("ELASTICSEARCH_HOSTS", "http://localhost:9200").split(","),
            "index_name": os.getenv("ELASTICSEARCH_INDEX", "rag_documents"),
        },
        "postgresql": {
            "connection_string": os.getenv("POSTGRESQL_URI", "postgresql://postgres:postgres@localhost:5432/rag_db"),
            "collection_name": os.getenv("POSTGRESQL_COLLECTION", "documents"),
        }
    }

    # Embedding model settings
    embedding_model_name: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    embedding_dimension: int = 384  # Default for all-MiniLM-L6-v2

    # Text splitting settings
    default_chunk_size: int = 1000
    default_chunk_overlap: int = 200

    # RAG enhancement settings
    use_hyde: bool = False
    use_reranking: bool = False
    use_doc_compression: bool = False

    # Create necessary directories
    def initialize(self):
        """Initialize necessary directories and resources."""
        self.data_dir.mkdir(exist_ok=True, parents=True)

        # Create vector store persistence directory if using Chroma
        if self.vector_store_type == "chroma":
            Path(self.vector_store_config["chroma"]["persist_directory"]).mkdir(exist_ok=True, parents=True)

        return self


# Create default application config
config = AppConfig().initialize()
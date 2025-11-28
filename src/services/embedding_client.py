"""Client for generating text embeddings using Google GenAI."""

import logging

from google import genai
from google.api_core.exceptions import GoogleAPIError
from google.genai.types import EmbedContentConfig

from config import config

logger = logging.getLogger(__name__)


class EmbeddingClient:
    """Client for generating text embeddings via Google GenAI."""

    EMBEDDING_MODEL = "gemini-embedding-001"
    EMBEDDING_DIMENSION = 512
    TASK_TYPE = "RETRIEVAL_QUERY"

    def __init__(self):
        """Initialize the embedding client with Vertex AI credentials."""
        self._client = genai.Client(
            vertexai=True,
            project=config.CYBERBIZ_GCP_PROJECT_ID,
            location=config.CYBERBIZ_GENAI_LOCATION
        )

    async def generate_embedding(self, text: str) -> list[float]:
        """
        Generate embedding vector for the given text.

        Args:
            text: Input text to generate embedding for

        Returns:
            List of float values representing the embedding vector

        Raises:
            GoogleAPIError: If API call fails (network, auth, rate limit, etc.)
            ValueError: If embedding generation returns empty or invalid results
        """
        try:
            logger.info(f"GenAI generating embedding for text: '{text[:100]}...'")

            response = await self._client.aio.models.embed_content(
                model=self.EMBEDDING_MODEL,
                contents=text,
                config=EmbedContentConfig(
                    output_dimensionality=self.EMBEDDING_DIMENSION,
                    task_type=self.TASK_TYPE
                ),
            )

            # Validate response
            if not response.embeddings or len(response.embeddings) == 0:
                error_msg = f"Embedding generation returned no results for text: '{text[:100]}...'"
                logger.error(f"{error_msg}, full response: {response}")
                raise ValueError(error_msg)

            embedding = response.embeddings[0]

            # Log token usage
            self._log_token_usage(embedding)

            # Validate embedding values
            if not embedding.values or len(embedding.values) == 0:
                error_msg = f"Embedding contains no values for text: '{text[:100]}...'"
                logger.error(f"{error_msg}, full response: {response}")
                raise ValueError(error_msg)

            logger.info(f"GenAI embedding generated successfully - dimension: {len(embedding.values)}")
            return embedding.values

        except GoogleAPIError as e:
            logger.error(f"GenAI API error while generating embedding: {str(e)}")
            raise

    def _log_token_usage(self, embedding) -> None:
        """Log token usage statistics for the embedding."""
        token_count = 0
        if hasattr(embedding, "statistics") and embedding.statistics:
            token_count = getattr(embedding.statistics, "token_count", 0)

        logger.info(
            f"GenAI Embedding Token Usage - "
            f"Model: {self.EMBEDDING_MODEL}, "
            f"Tokens: {token_count}"
        )

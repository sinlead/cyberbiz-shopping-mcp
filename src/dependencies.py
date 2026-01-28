"""Dependency injection providers for shared client instances."""

from functools import lru_cache

from google.cloud import bigquery

from config import config
from context import get_shop_id, get_shop_domain
from services.cyberbiz_bigquery_client import CyberbizBigQueryClient
from services.embedding_client import EmbeddingClient


@lru_cache(maxsize=1)
def get_embedding_client() -> EmbeddingClient:
    """
    Get the singleton EmbeddingClient instance.

    Cached because it's expensive to initialize and has no request-specific state.
    """
    return EmbeddingClient()


@lru_cache(maxsize=1)
def get_bigquery_base_client() -> bigquery.Client:
    """
    Get the singleton BigQuery client instance.

    Cached because BigQuery client is expensive to initialize (auth, connection setup).
    This base client is shared across all shops.
    """
    return bigquery.Client(project=config.CYBERBIZ_GCP_PROJECT_ID)


def get_bigquery_client() -> CyberbizBigQueryClient:
    """
    Get a BigQueryClient for the current request.

    Returns:
        CyberbizBigQueryClient instance with shop_id from request context

    Raises:
        ValueError: If shop_id is not available in request context
    """
    shop_id = get_shop_id()  # Get from request context
    return CyberbizBigQueryClient(
        client=get_bigquery_base_client(),
        shop_id=shop_id,
    )

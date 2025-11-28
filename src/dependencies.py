"""Dependency injection providers for shared client instances."""

from functools import lru_cache

from fastmcp.server.dependencies import get_access_token
from google.cloud import bigquery

from config import config
from services.cyberbiz_bigquery_client import CyberbizBigQueryClient
from services.cyberbiz_client import CyberbizClient
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
        CyberbizBigQueryClient instance with shop_id from access token

    Raises:
        ValueError: If no authentication token is available
    """
    token = get_access_token()
    if not token:
        raise ValueError("Authentication required for BigQuery operations")

    shop_id = 146 or token.claims.get("shop_id")  # FIXME: for dev
    return CyberbizBigQueryClient(
        client=get_bigquery_base_client(),
        shop_id=shop_id,
    )


def get_cyberbiz_client() -> CyberbizClient:
    """
    Get a CyberbizClient for the current request.

    Returns:
        CyberbizClient instance authenticated with current access token

    Raises:
        ValueError: If no authentication token is available
    """
    token = get_access_token()
    if not token:
        raise ValueError("Authentication required for Cyberbiz API operations")

    return CyberbizClient(token.token)

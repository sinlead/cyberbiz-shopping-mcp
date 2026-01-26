"""HTTP client for Cyberbiz API operations."""

import logging
from typing import Any, Dict

import httpx

from config import config

logger = logging.getLogger(__name__)


class CyberbizClient:
    """HTTP client for accessing Cyberbiz APIs with OAuth token."""

    def __init__(self, access_token: str):
        """
        Initialize Cyberbiz client with OAuth access token.

        Args:
            access_token: OAuth token for Cyberbiz API access
        """
        self.access_token = access_token
        self.base_url = config.cyberbiz_api_base_url
        self.timeout = 30

    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for Cyberbiz API requests."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def make_request(self, method: str, path: str, **kwargs) -> Any:
        """
        Make HTTP request to Cyberbiz API with error handling.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            path: API endpoint path (e.g., "/v2/products/123")
            **kwargs: Additional arguments passed to httpx (data, params, json, etc.)

        Returns:
            Parsed JSON response

        Raises:
            httpx.HTTPStatusError: If response status is 4xx or 5xx
            httpx.RequestError: If network/connection error occurs
            ValueError: If response is not valid JSON
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                url = f"{self.base_url}{path}"
                logger.info(f"Cyberbiz API request: {method.upper()} {url}")

                response = await client.request(
                    method,
                    url,
                    headers=self._get_headers(),
                    **kwargs
                )

                response.raise_for_status()

                logger.info(
                    f"Cyberbiz API response: {response.status_code} - "
                    f"Content length: {len(response.content)} bytes"
                )
                return response.json()

            except httpx.HTTPStatusError as e:
                error_detail = f"HTTP {e.response.status_code}"
                try:
                    error_body = e.response.json()
                    error_detail += f" - {error_body}"
                except Exception:
                    error_detail += f" - {e.response.text[:200]}"

                logger.error(f"Cyberbiz API HTTP error: {method.upper()} {url} - {error_detail}")
                raise

            except httpx.RequestError as e:
                logger.error(f"Cyberbiz API request failed: {method.upper()} {url} - {str(e)}")
                raise

            except ValueError as e:
                logger.error(f"Cyberbiz API returned invalid JSON: {method.upper()} {url} - {str(e)}")
                raise

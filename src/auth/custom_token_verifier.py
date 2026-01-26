"""Custom token verifier for CYBERBIZ OAuth tokens."""

import base64

import httpx
from fastmcp.server.auth.auth import AccessToken, TokenVerifier


class CustomIntrospectionVerifier(TokenVerifier):
    """
    Custom token verifier that calls cyberbiz.co introspection endpoint.
    Uses the MCP Server's OAuth client secret as API key for authentication.
    """

    def __init__(
        self,
        introspection_url: str,
        api_key: str,
        required_scopes: list[str] | None = None,
        timeout: int = 10,
    ):
        """
        Initialize the custom introspection verifier.

        Args:
            introspection_url: The introspection endpoint URL
            api_key: Credentials in format "client_id:client_secret" for
                    HTTP Basic Authentication with the introspection endpoint
            required_scopes: List of required scopes for the token
            timeout: Request timeout in seconds
        """
        self.introspection_url = introspection_url
        self.api_key = api_key
        self.required_scopes = required_scopes
        self.timeout = timeout

    async def verify_token(self, token: str) -> AccessToken | None:
        """
        Verify the token by calling the introspection endpoint.

        Args:
            token: The bearer token to verify

        Returns:
            AccessToken object containing claims and scopes, or None if invalid

        Raises:
            Exception: If token verification fails
        """
        async with httpx.AsyncClient() as client:
            try:
                # Encode credentials for HTTP Basic Authentication
                auth_string = base64.b64encode(self.api_key.encode()).decode()

                response = await client.post(
                    self.introspection_url,
                    headers={
                        "Authorization": f"Basic {auth_string}",
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    data={"token": token},
                    timeout=self.timeout,
                )

                if response.status_code == 401:
                    raise Exception("Unauthorized: Invalid client credentials")

                if response.status_code != 200:
                    raise Exception(
                        f"Introspection failed with status {response.status_code}: {response.text}"
                    )

                data = response.json()

                # Check if token is active
                if not data.get("active", False):
                    return None

                # Extract scopes
                scopes_str = data.get("scope", "")
                scopes = scopes_str.split() if scopes_str else []

                # Extract claims (custom fields from the introspection response)
                claims = {
                    "shop_id": data.get("shop_id"),
                    "shop_domain": data.get("shop_domain"),
                    "exp": data.get("exp"),
                }

                return AccessToken(
                    token=token,
                    client_id=data.get("client_id", ""),
                    scopes=scopes,
                    expires_at=data.get("exp"),
                    claims=claims,
                )

            except httpx.RequestError as e:
                raise Exception(f"Failed to connect to introspection endpoint: {e}")
            except Exception as e:
                raise Exception(f"Token verification failed: {e}")

"""Configuration settings for the MCP auth server."""

import os

from dotenv import load_dotenv

# Load .env file before reading environment variables
load_dotenv()


class Config:
    """Configuration class that loads from environment variables with sensible defaults."""

    # Server settings
    HOST: str = os.getenv("HOST", "")
    PORT: int = int(os.getenv("PORT", ""))
    TRANSPORT: str = os.getenv("TRANSPORT", "")

    # Public URL for OAuth metadata (only needed for dev with ngrok)
    # In production, this will be the same as the server's actual URL
    PUBLIC_URL: str = os.getenv("PUBLIC_URL", "")

    # OAuth settings
    CYBERBIZ_AUTH_HOST: str = os.getenv("CYBERBIZ_AUTH_HOST", "")
    CYBERBIZ_AUTH_PORT: str = os.getenv("CYBERBIZ_AUTH_PORT", "")
    CYBERBIZ_AUTH_PUBLIC_URL: str = os.getenv("CYBERBIZ_AUTH_PUBLIC_URL", "")
    CYBERBIZ_AUTH_AUDIENCE: str = os.getenv("CYBERBIZ_AUTH_AUDIENCE", "")

    # MCP Server OAuth client credentials (for introspection only)
    MCP_SERVER_CLIENT_ID: str = os.getenv("MCP_SERVER_CLIENT_ID", "")
    MCP_SERVER_CLIENT_SECRET: str = os.getenv("MCP_SERVER_CLIENT_SECRET", "")

    # Required scopes for different operations
    REQUIRED_SCOPES_CHECK_ORDER: str = "read_orders"

    @property
    def server_url(self) -> str:
        if self.PUBLIC_URL:
            return self.PUBLIC_URL
        return f"http://{self.HOST}:{self.PORT}"

    @property
    def auth_base_url(self) -> str:
        if self.CYBERBIZ_AUTH_PUBLIC_URL:
            return self.CYBERBIZ_AUTH_PUBLIC_URL
        return f"http://{self.CYBERBIZ_AUTH_HOST}:{self.CYBERBIZ_AUTH_PORT}"

    def validate(self) -> None:
        """Validate configuration."""
        if self.TRANSPORT not in ["sse", "streamable-http"]:
            raise ValueError(f"Invalid transport: {self.TRANSPORT}. Must be 'sse' or 'streamable-http'")

# Global configuration instance
config = Config()

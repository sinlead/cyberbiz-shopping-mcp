"""Configuration settings for the MCP auth server."""

import os

from dotenv import load_dotenv

# Load .env file before reading environment variables
load_dotenv(dotenv_path=os.getenv("ENV_FILE", ".env"))


class Config:
    """Configuration class that loads from environment variables with sensible defaults."""

    # Server settings
    HOST: str = os.getenv("HOST", "")
    PORT: int = int(os.getenv("PORT", ""))
    TRANSPORT: str = os.getenv("TRANSPORT", "")

    # Public URL for OAuth metadata (only needed for dev with ngrok)
    # In production, this will be the same as the server's actual URL
    PUBLIC_URL: str = os.getenv("PUBLIC_URL", "")

    # OAuth/Auth server
    CYBERBIZ_HOST: str = os.getenv("CYBERBIZ_HOST", "")
    CYBERBIZ_PORT: str = os.getenv("CYBERBIZ_PORT", "")
    CYBERBIZ_PUBLIC_URL: str = os.getenv("CYBERBIZ_PUBLIC_URL", "")

    # App Store API server
    CYBERBIZ_APP_STORE_API_HOST: str = os.getenv("CYBERBIZ_APP_STORE_API_HOST", "")
    CYBERBIZ_APP_STORE_API_PORT: str = os.getenv("CYBERBIZ_APP_STORE_API_PORT", "")

    # GCP for AI
    CYBERBIZ_GCP_PROJECT_ID: str = os.getenv("CYBERBIZ_GCP_PROJECT_ID", "")
    CYBERBIZ_GENAI_LOCATION: str = os.getenv("CYBERBIZ_GENAI_LOCATION", "")

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
        """Base URL for OAuth/auth endpoints."""
        if self.CYBERBIZ_PUBLIC_URL:
            return self.CYBERBIZ_PUBLIC_URL

        if self.CYBERBIZ_HOST.endswith(".lvh.me"):
            return f"http://{self.CYBERBIZ_HOST}:{self.CYBERBIZ_PORT}"
        else:
            return f"https://{self.CYBERBIZ_HOST}"

    @property
    def cyberbiz_api_base_url(self) -> str:
        """Base URL for App Store API endpoints."""
        if self.CYBERBIZ_APP_STORE_API_HOST.endswith(".lvh.me"):
            return f"http://{self.CYBERBIZ_APP_STORE_API_HOST}:{self.CYBERBIZ_APP_STORE_API_PORT}"
        else:
            return f"https://{self.CYBERBIZ_APP_STORE_API_HOST}"

    def validate(self) -> None:
        """Validate configuration."""
        if self.TRANSPORT not in ["sse", "streamable-http"]:
            raise ValueError(f"Invalid transport: {self.TRANSPORT}. Must be 'sse' or 'streamable-http'")

# Global configuration instance
config = Config()

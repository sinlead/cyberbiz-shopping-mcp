"""Configuration settings for the MCP server."""

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

    # Storefront API server (public API for products)
    STOREFRONT_API_HOST: str = os.getenv("STOREFRONT_API_HOST", os.getenv("CYBERBIZ_APP_STORE_API_HOST", ""))
    STOREFRONT_API_PORT: str = os.getenv("STOREFRONT_API_PORT", os.getenv("CYBERBIZ_APP_STORE_API_PORT", ""))

    # GCP for AI
    CYBERBIZ_GCP_PROJECT_ID: str = os.getenv("CYBERBIZ_GCP_PROJECT_ID", "")
    CYBERBIZ_GENAI_LOCATION: str = os.getenv("CYBERBIZ_GENAI_LOCATION", "")

    @property
    def storefront_api_base_url(self) -> str:
        """Base URL for Storefront API endpoints."""
        if self.STOREFRONT_API_HOST.endswith(".lvh.me"):
            return f"http://{self.STOREFRONT_API_HOST}:{self.STOREFRONT_API_PORT}"
        else:
            return f"https://{self.STOREFRONT_API_HOST}"

    # Backward compatibility
    @property
    def cyberbiz_api_base_url(self) -> str:
        """Base URL for Storefront API endpoints (deprecated, use storefront_api_base_url)."""
        return self.storefront_api_base_url

    def validate(self) -> None:
        """Validate configuration."""
        if self.TRANSPORT not in ["sse", "streamable-http"]:
            raise ValueError(f"Invalid transport: {self.TRANSPORT}. Must be 'sse' or 'streamable-http'")

# Global configuration instance
config = Config()

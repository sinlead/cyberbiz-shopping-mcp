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

    # GCP for AI
    CYBERBIZ_GCP_PROJECT_ID: str = os.getenv("CYBERBIZ_GCP_PROJECT_ID", "")
    CYBERBIZ_GENAI_LOCATION: str = os.getenv("CYBERBIZ_GENAI_LOCATION", "")

    def validate(self) -> None:
        """Validate configuration."""
        if self.TRANSPORT not in ["sse", "streamable-http"]:
            raise ValueError(f"Invalid transport: {self.TRANSPORT}. Must be 'sse' or 'streamable-http'")

# Global configuration instance
config = Config()

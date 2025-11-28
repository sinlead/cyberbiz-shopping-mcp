"""MCP server instance."""

import logging

from fastmcp import FastMCP
from fastmcp.server.auth import RemoteAuthProvider
from pydantic import AnyHttpUrl

from auth import CustomIntrospectionVerifier
from config import config

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# MCP server --> cyberbiz.co (as auth server)
# API key is the MCP Server's OAuth client secret from Doorkeeper

token_verifier = CustomIntrospectionVerifier(
    introspection_url=f"{config.auth_base_url}/mcp/oauth/introspect",
    api_key=f"{config.MCP_SERVER_CLIENT_ID}:{config.MCP_SERVER_CLIENT_SECRET}",
)

auth = RemoteAuthProvider(
    token_verifier=token_verifier,
    authorization_servers=[AnyHttpUrl(config.auth_base_url)],
    base_url=config.server_url,
)

mcp = FastMCP(
    name="CYBERBIZ-Shopping-MCP",
    instructions=(
        "AI shopping assistant for helping customers buy products and get support on the CYBERBIZ e-commerce platform."
    ),
    version="0.1.0",
    auth=auth,
)

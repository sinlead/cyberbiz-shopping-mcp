"""MCP server initialization and tool registration."""

from typing import cast

from fastmcp import FastMCP
from fastmcp.server.auth import RemoteAuthProvider
from fastmcp.server.server import Transport
from pydantic import AnyHttpUrl

from auth import CustomIntrospectionVerifier
from config import config
from tools import (
    cancel_order,
    check_order,
    check_purchase_feasibility,
    discover_products,
    handle_after_sales,
    modify_order,
    place_order,
)

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
        "AI shopping assistant for helping customers buy products "
        "and get support on the CYBERBIZ e-commerce platform."
    ),
    version="0.1.0",
    auth=auth,
    tools=[
        discover_products,
        check_purchase_feasibility,
        place_order,
        check_order,
        modify_order,
        cancel_order,
        handle_after_sales,
    ]
)

if __name__ == "__main__":
    mcp.run(cast(Transport, config.TRANSPORT))

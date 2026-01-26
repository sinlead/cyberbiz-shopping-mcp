"""MCP server initialization and tool registration."""
# ruff: noqa

from typing import cast
from fastmcp.server.server import Transport
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from config import config
from mcp_instance import mcp

# Import tools module to register all tools via decorators
import tools


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> Response:
    """Health check endpoint to verify the tool server is running."""
    return JSONResponse({"status": "ok", "service": "cyberbiz-shopping-mcp"})


if __name__ == "__main__":
    mcp.run(
        transport=cast(Transport, config.TRANSPORT),
        host=config.HOST,
        port=config.PORT,
    )

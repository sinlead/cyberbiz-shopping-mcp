"""MCP server initialization and tool registration."""
# ruff: noqa

from typing import cast
from fastmcp.server.server import Transport
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from config import config
from context import get_shop_id, get_shop_domain
from mcp_instance import mcp
from middleware import ShopContextMiddleware

# Import tools module to register all tools via decorators
import tools


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> Response:
    """Health check endpoint to verify the tool server is running."""
    return JSONResponse({"status": "ok", "service": "cyberbiz-shopping-mcp"})


@mcp.custom_route("/test/context", methods=["GET"])
async def test_context(request: Request) -> Response:
    """Test endpoint to verify shop context is extracted from headers and list available tools."""
    try:
        shop_id = get_shop_id()
        shop_domain = get_shop_domain()

        # Get list of registered tools
        tools_list = []
        for tool_name, tool in mcp.list_tools():
            tool_info = {
                "name": tool_name,
                "description": tool.description if hasattr(tool, 'description') else None,
            }
            tools_list.append(tool_info)

        return JSONResponse({
            "status": "success",
            "shop_id": shop_id,
            "shop_domain": shop_domain,
            "message": "Shop context successfully extracted from headers",
            "available_tools": tools_list,
            "total_tools": len(tools_list)
        })
    except ValueError as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=400)


if __name__ == "__main__":
    mcp.run(
        transport=cast(Transport, config.TRANSPORT),
        host=config.HOST,
        port=config.PORT,
        middleware=[Middleware(ShopContextMiddleware)],
    )

"""MCP server initialization and tool registration."""

from fastmcp import FastMCP
from mcp.types import Icon

from tools import (
    cancel_order,
    check_order,
    check_purchase_feasibility,
    discover_products,
    handle_after_sales,
    modify_order,
    place_order,
)

mcp = FastMCP(
    name="CYBERBIZ Shopping MCP",
    instructions=(
        "AI shopping assistant for helping customers buy products "
        "and get support on the CYBERBIZ e-commerce platform."
    ),
    version="0.1.0",
    website_url="https://www.cyberbiz.io/",
    icons=[
      Icon(
        src="https://www.cyberbiz.io/wp-content/uploads/2020/12/favi_512-150x150.png"
      )
    ],
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
    mcp.run()

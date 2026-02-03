"""MCP server instance."""

import logging

from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

mcp = FastMCP(
    name="CYBERBIZ-Shopping-MCP",
    instructions=(
        "AI shopping assistant for helping customers buy products and get support on the CYBERBIZ e-commerce platform."
    ),
    version="0.1.0",
)

"""MCP server initialization and tool registration."""
# ruff: noqa

from typing import cast
from fastmcp.server.server import Transport
from config import config
from mcp_instance import mcp

# Import tools module to register all tools via decorators
import tools

if __name__ == "__main__":
    mcp.run(cast(Transport, config.TRANSPORT))

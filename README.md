## Dev
- Install `uv`
- Setup
  ```sh
  uv venv
  source .venv/bin/activate
  uv sync
  ```
- Manage depedencies
  ```sh
  uv add <package>
  uv remove <package>
  ```
- Run server locally
  ```sh
  fastmcp run src/server.py --transport http --port 8000
  ```

## Claude Desktop Example
- Make sure uv is installed via brew so that Claude Desktop can pick it up
  ```sh
  brew install uv
  ```
- Install the MCP server to Claude Desktop
  ```sh
  fastmcp install claude-desktop src/server.py --env-file .env
  ```
- Make sure the MCP server is running
- Open up Claude Desktop

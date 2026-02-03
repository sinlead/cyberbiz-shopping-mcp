## Setup
- Install `uv`
- Install depedencies
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
- Configure environment variables in .env
  ```sh
  # MCP Server Configuration
  HOST=localhost
  PORT=8000
  TRANSPORT=streamable-http

  # GCP Configuration for AI Services
  CYBERBIZ_GCP_PROJECT_ID=your-gcp-project-id
  CYBERBIZ_GENAI_LOCATION=us-central1
  ```
- Run server locally
  ```sh
  python src/server.py # using default .env file
  ENV_FILE=.env.staging python src/server.py # specify env file
  ```

## Claude Desktop Example（Paid version）
- Make sure the MCP server is running
- Open up Claude Desktop
- Go to Profile (Bottom Left) > Settings > Connectors > Add custom connector
  - Name: `CYBERBIZ Shopping MCP`
  - Remote Sever URL: `<your MCP server URL>/mcp`
- Configure the MCP client to include required HTTP headers:
  - `X-Shop-ID`: Your shop's unique identifier (integer)
  - `X-Shop-Domain`: Your shop's domain (e.g., `yourshop.cyberbiz.co`)
- Start asking questions to trigger those tools!

## Authentication
This MCP server uses HTTP header-based authentication. The server expects the following headers in each request:

- `X-Shop-ID`: The unique identifier for the shop (integer)
- `X-Shop-Domain`: The shop's domain (e.g., `yourshop.cyberbiz.co`)

These headers are validated by the [ShopContextMiddleware](src/middleware.py) and used to establish the shop context for all tool operations.

### How it works

```
┌─────────────────┐
│  MCP Client     │  (e.g., Claude Desktop)
└────────┬────────┘
         │
         │ HTTP Request with headers:
         │ X-Shop-ID: 123
         │ X-Shop-Domain: shop.cyberbiz.co
         │
         ▼
┌─────────────────┐
│   MCP Server    │
│                 │
│  Middleware     │  1. Extract headers
│  validates &    │  2. Validate shop_id & shop_domain
│  sets context   │  3. Set context for request
│                 │
│  Tools execute  │  4. Use shop context for API calls
│  with shop      │     to Storefront API
│  context        │
└─────────────────┘
```

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
- change .env
  ```.sh
  # 去 EC Rails console 創建專屬於 MCP Server 的 OAuth Application
  app = Doorkeeper::Application.create!(
    name: "CYBERBIZ Shopping MCP Server",
    redirect_uri: "urn:ietf:wg:oauth:2.0:oob",  # 表示不需要 redirect
    confidential: true, # server-to-server
  )

  # 顯示 credentials
  puts "Client ID: #{app.uid}"
  puts "Client Secret: #{app.secret}"

  # 將 credentials 放到 MCP_SERVER_CLIENT_ID, MCP_SERVER_CLIENT_SECRET
  ```
- 使用 zrok 來把本地的 MCP server 以及本地的 Auth/Resource Server (cyberbiz.co) 暴露到外網，以利各 AI assistant 連接
  ```sh
  zrok share public localhost:8000  # 把此 zrok 網域放到 PUBLIC_URL
  zrok share public www.lvh.me:4000  # 把此 zrok 網域放到 CYBERBIZ_PUBLIC_URL
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
  - Remote Sever URL: `<url you get from "zrok share public localhost:8000">/mcp` （note that there's an appended /mcp in the end）
- Click 'Connect' > Enter shop domain > Login > Approve at consent window
- Start asking questions to trigger those tools!

## How OAuth works
We use follow DCR(Dynamic Client Registration) to allow agent discover & register OAuth client automatically. MCP server is also responsible for verify the token passed by MCP client, by delegating to introspection endpoint of auth server (which is cyberbiz.co for now).

1. MCP Server 自己（固定的、預先創建的）

- 目的：讓 MCP Server 可以呼叫 introspection endpoint 驗證 token
- 創建方式：你手動在 Doorkeeper 創建（用 Rails console）
- Credentials：
  - MCP_SERVER_CLIENT_ID
  - MCP_SERVER_CLIENT_SECRET
- 用途：只用於 server-to-server 的 introspection 呼叫

2. 每個 MCP Client（動態註冊的、多個）

- 目的：讓終端用戶（如 Claude Desktop）可以透過 OAuth 2.0 flow 取得 access token
- 創建方式：透過 DCR (Dynamic Client Registration) 自動創建
- 數量：每個 MCP Client 實例都是一個獨立的 OAuth client
- 用途：執行 authorization code flow，取得代表用戶的 access token

完整流程

┌─────────────────┐
│  MCP Client     │  (例如：Claude Desktop)
│  (用戶裝置)      │
└────────┬────────┘
          │
          │ 1. DCR (Dynamic Client Registration)
          ├──────────────────────────────────────┐
          │                                      │
          │  POST /oauth/register                │
          │  → 取得自己的 client_id/secret       │
          │                                      │
          │ 2. OAuth Authorization Flow          ▼
          ├─────────────────────────────► ┌──────────────┐
          │                               │ cyberbiz.co  │
          │  /oauth/authorize             │ (Auth Server)│
          │  /oauth/token                 └──────┬───────┘
          │  ← 用戶授權後取得 access_token       │
          │                                      │
          │ 3. 呼叫 MCP Server tools             │
          │    (帶著 access_token)               │
          ▼                                      │
┌─────────────────┐                             │
│   MCP Server    │                             │
│                 │  4. Token Introspection     │
│                 ├─────────────────────────────┘
│                 │  POST /mcp/oauth/introspect
│                 │  Authorization: Basic base64(
│                 │    MCP_SERVER_CLIENT_ID:
│                 │    MCP_SERVER_CLIENT_SECRET
│                 │  )
│                 │  ← 驗證 token 是否有效
└─────────────────┘

在 Doorkeeper 中會看到的 Applications

| Name                         | Purpose                 | 創建方式        |
|------------------------------|-------------------------|-------------|
| CYBERBIZ Shopping MCP Server | 用於 introspection        | 你手動創建（只有一個） |
| Claude Desktop - User A      | User A 的 Claude Desktop | DCR 自動創建    |
| Claude Desktop - User B      | User B 的 Claude Desktop | DCR 自動創建    |
| Custom MCP Client            | 其他 MCP 客戶端              | DCR 自動創建    |

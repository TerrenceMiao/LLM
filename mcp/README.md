MCP (Model Context Protocol)
============================

- Google Maps

![MCP - Google Maps](MCP%20-%20Google%20Maps.png)

```
{
  "mcpServers": {
    "github.com/modelcontextprotocol/servers/tree/main/src/google-maps": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-google-maps"
      ],
      "env": {
        "GOOGLE_MAPS_API_KEY": "AIza ... 89S4"
      },
      "disabled": false,
      "autoApprove": [
        "maps_geocode",
        "maps_search_places"
      ]
    }
  }
}
```

Question _**Discover the top 3 best Vietnamese Pho spots located between Yarraville and Melbourne CBD**_ in `Cline` MCP Servers.

![MCP - Google Maps in action](MCP%20-%20Google%20Maps%20in%20action.png)

- Weather

![MCP - Weather](MCP%20-%20Weather.png)

in `Claude Desktop` configuration file at **~/Library/Application Support/Claude/claude_desktop_config.json**, and logs under **~/Library/Logs/Claude**:

```
{
  "mcpServers": {
    "weather": {
      "command": "/Users/terrence/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/terrence/Projects/LLM/mcp",
        "run",
        "weather.py"
      ]
    }
  }
}
```
![MCP - Weather MCP Tools](MCP%20-%20Weather%20MCP%20Tools.png)

![MCP - Weather Allow MCP Tools](MCP%20-%20Weather%20Allow%20MCP%20Tools.png)

![MCP - Weather in New York](MCP%20-%20Weather%20in%20New%20York.png)

- Hello MCP

![MCP - Hello MCP](MCP%20-%20Hello%20MCP.png)

- Remote MCP Server

Base on the blog **Build and deploy Remote Model Context Protocol (MCP) servers to Cloudflare** _https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/_, a Remote MCP Server example, which is a worker runs in Cloudflare _https://remote-mcp-server.terrence-miao.workers.dev_.

Input MCP Server URL _https://remote-mcp-server.terrence-miao.workers.dev/sse_ with Transport Type set to **SSE** (Server-Sent Events):

![MCP - Remote MCP Server](MCP%20-%20Remote%20MCP%20Server.png)

```
{
  "mcpServers": {
    "weather": {
      "command": "/usr/local/bin/npx",
      "args": [
        "mcp-remote",
        "https://remote-mcp-server.terrence-miao.workers.dev/sse"
      ]
    }
  }
}
```

![MCP - Remote MCP Server math tool](MCP%20-%20Remote%20MCP%20Server%20math%20tool.png)

![MCP - Remote MCP Server authorised](MCP%20-%20Remote%20MCP%20Server%20authorised.png)

![MCP - Remote MCP Server in action](MCP%20-%20Remote%20MCP%20Server%20in%20action.png)


References
----------

- MCP For Server Developers, _https://modelcontextprotocol.io/quickstart/server_
- Building MCP Servers, _https://medium.com/@cstroliadavis/building-mcp-servers-536969d27809_
- Google Maps MCP, _https://github.com/modelcontextprotocol/servers/tree/main/src/google-maps_
- MCP CLI, _https://github.com/wong2/mcp-cli_
- MCP Inspector, _https://github.com/modelcontextprotocol/inspector_
- Cloudflare AI Playground, _https://playground.ai.cloudflare.com/_
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

MCP Server - **Weather** configuration setup in `Claude Desktop` on Mac:

![MCP - Weather](MCP%20-%20Weather.png)

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

References
----------

- MCP For Server Developers, _https://modelcontextprotocol.io/quickstart/server_
- Building MCP Servers, _https://medium.com/@cstroliadavis/building-mcp-servers-536969d27809_
- Google Maps MCP, _https://github.com/modelcontextprotocol/servers/tree/main/src/google-maps_
- MCP CLI, _https://github.com/wong2/mcp-cli_

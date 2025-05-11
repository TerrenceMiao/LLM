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

- Playwright MCP

Login an authentication required site with username and password.

```
{
  "mcpServers": {
    "github.com/executeautomation/mcp-playwright": {
      "command": "npx",
      "args": ["-y", "@executeautomation/playwright-mcp-server"],
      "disabled": false,
      "autoApprove": [
        "start_codegen_session",
        "playwright_navigate",
        "clear_codegen_session",
        "playwright_fill",
        "playwright_click",
        "playwright_screenshot",
        "end_codegen_session",
        "playwright_get_visible_html",
        "playwright_press_key"
      ]
    }
  }
}
```

Input and invoke Playwright MCP Server:

```
- Navigate to `https://portal.microsoft.com/`
- Login with username `me@paradise.org` and password `blah` then click `Next` button
- Click `No` button when asked `Stay signed in?`
- Take a screenshot after successfully land on `Home` page
- Logout
- Click on the username when asked `Pick an account`
- Generate above steps into Playwright test code
```

![MCP - Playwright CLINE](MCP%20-%20Playwright%20CLINE.png)

![MCP - Playwright Sign in](MCP%20-%20Playwright%20Sign%20in.png)

![MCP - Playwright Enter your password](MCP%20-%20Playwright%20Password%20input.png)

![MCP - Playwright Stay signed in](MCP%20-%20Playwright%20Stay%20in.png)

![MCP - Playwright Home](MCP%20-%20Playwright%20Home.png)

![MCP - Playwright Sign out](MCP%20-%20Playwright%20Sign%20out.png)

![MCP - Playwright Pick an account](MCP%20-%20Playwright%20Pick.png)

`Playwright` test code:

```
import { test } from '@playwright/test';
import { expect } from '@playwright/test';

test('Microsoft Portal Login', async ({ page, context }) => {

    // Navigate to URL
    await page.goto('https://portal.microsoft.com/');

    // Fill input field for username
    await page.fill('input[type="email"]', 'me@paradise.org');

    // Click Next button
    await page.click('input[type="submit"]');

    // Add a small delay to help avoid "Too Many Requests" error
    await page.waitForTimeout(5000); // Wait for a few seconds (adjust as needed)

    // Fill input field for password using its ID
    await page.locator('#passwordEntry').fill('blah');

    // Click Next button for "Enter your password" using ARIA role and name
    await page.getByRole('button', { name: 'Next' }).click();

    // Click No button for "Stay signed in?" using data-testid
    await page.waitForTimeout(10000);
    await page.getByTestId('secondaryButton').click();

    // Take screenshot of the Home page
    await page.waitForTimeout(10000);
    await page.screenshot({ path: 'Microsoft Portal Home Screenshot.png', fullPage: true });

    // Click profile icon
    await page.click('[aria-label*="profile"], [aria-label*="Account"]');

    // Click Sign out link
    await page.click('//a[normalize-space()="Sign out"]');

    // Click username on "Pick an account" page
    await page.click('//*[contains(text(), "me@paradise.org")]');
});
```
![MCP - Playwright Test](MCP%20-%20Playwright%20Test.png)

To run the test:

```
$ npx playwright test test.spec.ts --headed
```

References
----------

- MCP For Server Developers, _https://modelcontextprotocol.io/quickstart/server_
- Building MCP Servers, _https://medium.com/@cstroliadavis/building-mcp-servers-536969d27809_
- Google Maps MCP, _https://github.com/modelcontextprotocol/servers/tree/main/src/google-maps_
- MCP CLI, _https://github.com/wong2/mcp-cli_
- MCP Inspector, _https://github.com/modelcontextprotocol/inspector_
- Cloudflare AI Playground, _https://playground.ai.cloudflare.com/_
- Playwright MCP Server 🎭, _https://github.com/executeautomation/mcp-playwright_
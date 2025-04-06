from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig

from pydantic import SecretStr

import os

from dotenv import load_dotenv

load_dotenv(".env.local")
load_dotenv()

import asyncio

# Basic configuration
browser_context_config = BrowserContextConfig(
    cookies_file="cookies.json",
)
browser_config = BrowserConfig(
    # new_context_config=browser_context_config,
    chrome_instance_path="/Applications/Chromium.app/Contents/MacOS/Chromium",
)
browser = Browser(config=browser_config)

# Initialize the model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite-001", api_key=SecretStr(os.getenv("GEMINI_API_KEY"))
)

task = """
    Compare the price of gpt-4o and DeepSeek-V3
"""

task = """
    Go to https://entra.microsoft.com/ and login as user terrence.miao@gmail.com.
    Click on 'Send notification' button in 'Sign in to continue to Microsoft Entra' dialog window.
    Stay on 'Check your Authentication App' dialog window and wait for authentication successfully.
    Then in the next 'Stay signed in' dialog window click on 'Yes' button.
    Take a screenshot after successful login.
"""

task = """
    Go to https://entra.microsoft.com/
    Search for 'Terrence Miao'
    Click on 'Terrence Miao' on search result
    Wait for user's Overview page to load
    Click on 'Properties' button
"""


# Create agent with the model
async def main():
    agent = Agent(
        browser=browser,
        task=task,
        llm=llm,
        use_vision=True,
        max_actions_per_step=20,
        retry_delay=5,
    )
    result = await agent.run()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from pydantic import SecretStr

import os

from dotenv import load_dotenv

load_dotenv(".env.local")
load_dotenv()

import asyncio

# Basic configuration
browser_config = BrowserConfig(
    headless=False,
    disable_security=True
)

browser = Browser(config=browser_config)

# Initialize the model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite-001", api_key=SecretStr(os.getenv("GEMINI_API_KEY"))
)

task = """
    Go to https://entra.microsoft.com/ and login as user terrence.miao@gmail.com.

    Click on 'Send notification' button in 'Sign in to continue to Microsoft Entra' dialog window.

    Stay on 'Check your Authentication App' dialog window and wait for authentication successfully.

    Then in the next 'Stay signed in' dialog window click on 'Yes' button.

    Take a screenshot after successful login.
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

if __name__ == '__main__':
    asyncio.run(main())

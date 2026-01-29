from browser_use import Agent, Browser
from browser_use.llm import ChatGoogle, ChatOllama, ChatOpenAI, ChatGroq

import os

from dotenv import load_dotenv

load_dotenv(".env.local")
load_dotenv()

import asyncio

# Basic configuration
# browser = Browser(
#     storage_state="cookies.json",
#     executable_path="/Users/terrence/Library/Caches/ms-playwright/chromium-1200/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
# )
browser = Browser(
    # cdp_url='http://localhost:9222'
)

# Initialize the model
# llm = ChatGoogle(
#     model="gemini-flash-lite-latest",
#     api_key=os.getenv("GEMINI_API_KEY")
# )
# llm = ChatOpenAI(
#     model="gemini-2.5-flash",
#     api_key="sk-",
#     base_url="http://localhost:10000",
# )
# llm = ChatOllama(
#     model="glm-4.7-flash",
# )
llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY"),
)

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

task = """
    Compare the price of gpt-4o and DeepSeek-V3
"""

# Create agent with the model
async def main():
    agent = Agent(
        browser=browser,
        task=task,
        llm=llm,
        use_vision=True,
        max_actions_per_step=20,
    )
    result = await agent.run()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())

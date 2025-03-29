from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import SecretStr

import os

from dotenv import load_dotenv

load_dotenv(".env.local")
load_dotenv()

import asyncio

# Initialize the model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite-001",
    api_key=SecretStr(os.getenv("GEMINI_API_KEY"))
)


# Create agent with the model
async def main():
    agent = Agent(
        task=(
            "Go to https://entra.microsoft.com/ and login as user terrence.miao@gmail.com. "
            "Click on 'Send notification' button in 'Sign in to continue to Microsoft Entra' dialog window. "
            "Stay on 'Check your Authentication App' dialog window and wait for authentication successfully. "
            "Then in the next 'Stay signed in' dialog window click on 'Yes' button. "
            "Take a screenshot after successful login."
        ),
        llm=llm,
    )
    result = await agent.run()
    print(result)


asyncio.run(main())

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import SecretStr

import os

from dotenv import load_dotenv
load_dotenv(".env.local")
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

import asyncio

# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.5-pro-exp-03-25', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))

# Create agent with the model
async def main():
    agent = Agent(
        task="Get the price of M4 MacBook Air 15 inch",
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())

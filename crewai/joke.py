"""
"Tell a joke" by using Crew AI. Run:

$ python joke.py

References

- Building an AI Dream Team with CrewAI - Even Better than AutoGEN? https://www.youtube.com/watch?v=LBnFe5FsuHc
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv() # take environment variables from .env.

openai_llm = ChatOpenAI(
    model_name = "gpt-3.5-turbo",
    temperature = 0
)

ollama_llm = Ollama(model="qwen:14b")

# LM Studio
# Better with model Mixtral-8x7B-Instruct-v0.1-GGUF / mixtral-8x7b-instruct-v0.1.Q5_K_M
local_llm = OpenAI(
    base_url = "http://localhost:1234/v1",
    api_key = "null",
    temperature = 0,
)

default_llm = ollama_llm

bob = Agent(
    role = "Bob",
    goal = "Telling a joke",
    backstory ="You love telling jokes.",
    llm = default_llm,
    verbose = True,
)

alice = Agent(
    role = "Alice",
    goal = "Criticizing a joke",
    backstory = "You love criticizing jokes.",
    llm = default_llm,
    verbose = True,
)

tell_joke = Task(
    description = "Tell a joke",
    agent = bob,
)

criticize_joke = Task(
    description = "Criticize joke Bob tells",
    agent = alice,
)

crew = Crew(
    agents = [bob, alice],
    tasks = [tell_joke, criticize_joke],
    verbose = 2, # You can set it to 1 or 2 to different logging levels
)

result = crew.kickoff()

# print(result)

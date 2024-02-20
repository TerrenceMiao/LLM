""""
To run:

$ streamlit run research_advanced.py

Reference: CrewAI Unleashed: Crafting Intelligent Crews from Scratch, https://www.youtube.com/watch?v=jHJar6hYBL4
"""

import os
import openai
import streamlit as st

from crewai import Agent, Task, Crew, Process
from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

## OpenAI
openai_llm = ChatOpenAI(
    temperature=0,
)

## Ollama
ollama_llm = Ollama(model="qwen:14b")

## LM Studio
## OpenHermes-2.5-Mistral-7B-GGUF / openhermes-2.5-mistral-7b.Q4_K_M could generate the best result
local_llm = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="null",
    temperature=0,
)

default_llm = ollama_llm

search_tool = DuckDuckGoSearchRun()

st.title("📝 Research & Write with AI Agents")

# Topics input like "Precision Nutrition and Longevity" or "AutoGen Agents"
topic = st.text_input("Topic")

if st.button("Research & Write"):
    researcher = Agent(
        role="Senior Researcher",
        goal=f"Uncover groundbreaking technologies around {topic}",
        backstory="Drive by curiosity, you're at the forefront of innovation",
        llm=default_llm,
        verbose=True,
    )

    writer = Agent(
        role="Writer",
        goal=f"Narrate compelling tech stories about {topic}",
        backstory="With a flair for simplifying complext topics, you craft engaging narratives.",
        llm=default_llm,
        verbose=True,
    )

    research_task = Task(
        description=f"""
            Identify the next big trend in {topic}.
            Focus on identifying pros and cons and the overall narrative.

            Your final report should clearly articulate the key points,
            its market opportunities, and potential risks.
        """,
        expected_output="A 3 paragraphs long report on the latest AI trends.",
        max_iter=1,
        tools=[search_tool],
        agent=researcher,
    )

    write_task = Task(
        description=f"""
            Compose an insightful article on {topic}.
            Focus on the latest trends and how it's impacting the industry.
            This article should be easy to understand, engaging and positive.
        """,
        expected_output=f"A 4 paragraph article on {topic} advancements",
        tools=[search_tool],
        agent=writer,
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
    )

    result = crew.kickoff()

    st.write(result)

from crewai import Crew
from tasks import MeetingPreparationTasks
from agents import MeetingPreparationAgents

import streamlit as st

tasks = MeetingPreparationTasks()
agents = MeetingPreparationAgents()

st.title("Meeting Prep")

participants = st.text_input(
    "What are the emails for the participants (other than you) in the meeting?\n"
)
context = st.text_input("What is the context of the meeting?\n")
objective = st.text_input("What is your objective for this meeting?\n")

# print(f"participants: {participants} | context: {context} | objective: {objective}")

if st.button("Start Generation"):

    researcher_agent = agents.research_agent()
    industry_analyst_agent = agents.industry_analysis_agent()
    meeting_strategy_agent = agents.meeting_strategy_agent()
    summary_and_briefing_agent = agents.summary_and_briefing_agent()

    research = tasks.research_task(researcher_agent, participants, context)
    industry_analysis = tasks.industry_analysis_task(
        industry_analyst_agent, participants, context
    )
    meeting_strategy = tasks.meeting_strategy_task(
        meeting_strategy_agent, context, objective
    )
    summary_and_briefing = tasks.summary_and_briefing_task(
        summary_and_briefing_agent, context, objective
    )

    crew = Crew(
        agents=[
            researcher_agent,
            industry_analyst_agent,
            meeting_strategy_agent,
            summary_and_briefing_agent,
        ],
        tasks=[research, industry_analysis, meeting_strategy, summary_and_briefing],
    )

    result = crew.kickoff()

    st.markdown(result)
    st.download_button(
        label="Download", data=result, file_name="meeting.md", mime="text/plain"
    )

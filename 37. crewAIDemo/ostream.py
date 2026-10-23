# python -m streamlit run ostream.py
import streamlit as st
from crewai import Task, Crew, Process, Agent, LLM
from tools import *
from dotenv import load_dotenv
import os

load_dotenv()

st.title("🤖 CrewAI Agent")

llm = LLM(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4.1-mini",
    temperature=1
)

additionAgent = Agent(
    role="addition expert of 2 numbers",
    goal="Add 2 numbers and return their sum",
    backstory="You are an expert at addition",
    llm=llm,
    tools=[addNumbers]
)

multiplicationAgent = Agent(
    role="multiplication expert of 2 numbers",
    goal="Multiply 2 numbers and return their product",
    backstory="You are an expert at multiplication",
    llm=llm,
    tools=[multiNumbers]
)

saveFileAgent = Agent(
    role="SaveFile expert",
    goal="Save content to hello.txt",
    backstory="You are an expert at saving files",
    llm=llm,
    tools=[saveFile]
)

readFileAgent = Agent(
    role="ReadFile expert",
    goal="Read content from hello.txt",
    backstory="You are an expert at reading files",
    llm=llm,
    tools=[readFile]
)

manager_agent = Agent(
    role="Manager",
    goal="Delegate work to the appropriate agent",
    backstory="You are an expert at delegating tasks",
    llm=llm
)

user_input = st.text_input("You:")

if st.button("Submit") and user_input:
    with st.spinner("Agent is working..."):
        task = Task(
            description=user_input,
            expected_output="A clear response to the user's request"
        )

        crew = Crew(
            agents=[
                additionAgent,
                multiplicationAgent,
                saveFileAgent,
                readFileAgent
            ],
            tasks=[task],
            manager_agent=manager_agent,
            process=Process.hierarchical,
            verbose=False
        )

        result = crew.kickoff()

    st.subheader("🤖 Agent Response")
    st.write(result.raw)
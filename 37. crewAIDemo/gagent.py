import os
os.environ["CREWAI_TRACING_ENABLED"] = "false"

from crewai import Task, Crew, Process, Agent, LLM
from dotenv import load_dotenv
from tools import *

load_dotenv()

llm = LLM(
    model="gemini-3.1-flash-lite",
    api_key=os.getenv("gemini_key")
)

additionAgent = Agent(
    role="Addition Expert",
    goal="Add two numbers",
    backstory="You are an expert in addition.",
    llm=llm,
    tools=[addNumbers]
)

multiplicationAgent = Agent(
    role="Multiplication Expert",
    goal="Multiply two numbers",
    backstory="You are an expert in multiplication.",
    llm=llm,
    tools=[multiNumbers]
)

saveFileAgent = Agent(
    role="Save File Expert",
    goal="Save content to hello.txt",
    backstory="You save content to local files.",
    llm=llm,
    tools=[saveFile]
)

readFileAgent = Agent(
    role="Read File Expert",
    goal="Read content from hello.txt",
    backstory="You read content from local files.",
    llm=llm,
    tools=[readFile]
)

manager_agent = Agent(
    role="Manager",
    goal="Delegate tasks to the correct agent",
    backstory="You manage and delegate tasks.",
    llm=llm
)

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    task = Task(
        description=user_input,
        expected_output="A clear and accurate result."
    )

    crew = Crew(
        agents=[additionAgent, multiplicationAgent, saveFileAgent, readFileAgent],
        tasks=[task],
        manager_agent=manager_agent,
        process=Process.hierarchical,
        verbose=False
    )

    result = crew.kickoff()
    print("\nAgent:", result.raw)
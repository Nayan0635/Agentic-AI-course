import os
os.environ["CREWAI_TRACING_ENABLED"] = "false"

from crewai import Task, Crew, Process, Agent, LLM
from tools import *
from dotenv import load_dotenv
load_dotenv()
#Connect to LLM i.e openai
llm = LLM(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4.1-mini",
    temperature=1
)

#Create Agent1 -->AdditionAgent
additionAgent = Agent(
    role="addition expert of 2 numbers",
    goal="addition of 2 numbers and returns their sum",
    backstory="You are expert of adding 2 numbers",
    llm=llm,
    tools=[addNumbers]
)
#Create 2nd Agent i.e MultiPlicationAgent
multiplicationAgent = Agent(
    role="multiplication expert of 2 numbers",
    goal="multiplication of 2 numbers and returns their product",
    backstory="You are expert of multiplying 2 numbers",
    llm=llm,
    tools=[addNumbers]
)
saveFileAgent = Agent(
    role="SaveFile expert",
    goal="saving content to  local file i.e hello.txt",
    backstory="You are an expert of saving content to local file",
    tools =[saveFile],
    llm =llm
)

readFileAgent = Agent(
    role="ReadFile expert",
    goal="reading content from created file i.e hello.txt",
    backstory="You are an expert of reading content from local file",
    tools =[readFile],
    llm =llm
)
#Now we need to create Manager Agent.
manager_agent = Agent(
    role="Manager Expert for delegating work to sub agents",
    goal="Delegating to proper and suitable Agent depends on user's prompt",
    backstory="You are an expert Manager for Delegating work",
    llm=llm
)

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    task = Task(
        description=user_input,
        expected_output="A clear response to the user's request."
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


# #Defined the Task for the CrewAI
# task = Task(
#     description=input("You :"),
#     expected_output="tools returns output"
# )

# #Build the entire crewAI Team
# crew = Crew(
#     agents=[additionAgent,multiplicationAgent,saveFileAgent,readFileAgent],
#     tasks=[task],
#     manager_agent=manager_agent,
#     process=Process.hierarchical,
#     #verbose=True
# )

# result = crew.kickoff()
# print("Agent :",result.raw)

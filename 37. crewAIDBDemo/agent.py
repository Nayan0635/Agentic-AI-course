import os
os.environ["CREWAI_TRACING_ENABLED"] = "false"
from crewai import LLM,Task,Crew,Process,Agent
from dotenv import load_dotenv
from tools import *
load_dotenv()
#Connecting to OpenAI
llm = LLM(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4.1-mini",
    temperature=0
)

#Creating the Database agents
addNewStudentAgent = Agent(
    role="adding new Student into the Database expert",
    goal="adding new student with their course details into sqlite3 database",
    backstory="You are an Database Insert Expert",
    tools=[addNewStudent],
    llm=llm
)

getAllStudentsAgent = Agent(
    role="Getting all students from the Database--> expert",
    goal="getting all students details along with their courses details from sqlite3 database",
    backstory="You are an Database Read Expert",
    tools=[getAllStudents],
    llm=llm
)


manager_agent = Agent(
    role="Delegates work expert to sub agents",
    goal="Delegating work depends on user's prompt to proper coworker agent",
    backstory="You are an expert Manager for delegating task to proper sub agents",
    llm=llm
)



while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    
    task = Task(
        description=user_input,
        expected_output="Tools returned output"
    )

    #Create the crew collaborative Team
    crew = Crew(
        agents=[addNewStudentAgent,getAllStudentsAgent],
        tasks=[task],
        manager_agent=manager_agent,
        process=Process.hierarchical
    )
    
    result = crew.kickoff()
    print("Agent :",result.raw)

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import PromptTemplate
from function import sendMail
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatNVIDIA(
    api_key = os.getenv("nvidia_key"),
    model = "meta/muse-glimmer-30b",
)

llm = llm.bind_tools([sendMail])

while True:
    user_input = input("Ask: ")
    if user_input.lower() == 'quit':
        print("Agent: GoodBye!")
        exit(0)
    
    prompt = PromptTemplate(
        template = '''
        Please modify the body of the email intelligently.

        Rules:
        - Make the message professional and polite.
        - Correct grammar and spelling.
        - Keep the message short and meaningful.
        - Do not change the original intention.
        - Then send the email using the sendMail tool.
        user's request: {user_input}''',
        input_variables = ["user_input"]
    )
    
    myMessage = prompt.invoke({"user_input": user_input})
    responses = llm.invoke(myMessage)
    
    if responses.tool_calls:
        tool_name = responses.tool_calls[0]['name']
        tool_args = responses.tool_calls[0]['args']
        
        if tool_name == "sendMail":
            result = sendMail.invoke(tool_args)
            print("Agent:", result)
        else:
            print("I can't help you except sending mail.")

# read time out
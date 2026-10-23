from openai import OpenAI
from dotenv import load_dotenv
import os
# from mcp.client.session import ClientSession
# from mcp.client.stdio import stdio_client,StdioServerParameters
from mcp import Client, StdioServerParameters

import asyncio
import json
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
print("OpenAI is connected")
#Connecting to MCP server.
server = StdioServerParameters(
    command="python",
    args=['server.py']
)
print("MCP server is connected")

async def callAgent():
    async with Client(server) as session:
        #getting all tools from mcp server.
        tools = await session.list_tools()
        print("Available tools:")
        #Now we need to convert this into openai tools
        openai_tools =[] #empty list
        for tool in tools.tools:
            print("tool :"+tool.name)
            openai_tools.append({
                "type":"function",
                "function":{
                    "name":tool.name,
                    "description":tool.description,
                    "parameters":tool.input_schema
                }
            })
        #Connecting to OpenAI
        user_input= input("You:")
        responses = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{
                "role":"user","content":user_input
            }],
            tools=openai_tools
        )
        message = responses.choices[0].message
        #Then we need to check whether tool gets called or not
        if message.tool_calls:
            toolName = message.tool_calls[0].function.name
            toolArgs = json.loads(message.tool_calls[0].function.arguments)
            result = await session.call_tool(toolName,toolArgs)
            print("Tool:"+toolName)
            print("toolArgs"+str(toolArgs))
            # print("RagContent"+result.content[0].text)
            ragContent = result.content[0].text
            #Now sending again to llm.
            responses2 = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{
                    "role":"user","content":f'''
                        -Context :{ragContent}
                        -Question :{user_input}
                        -Please use above context to answer only. 
                        '''
                }]
            )
            final_reply = responses2.choices[0].message.content
            print("AI Final Response :",final_reply)
        else:
            print("Agent: Sorry I can only provide information about Ejobindia")     


if __name__ == "__main__":
    # asyncio.run(main=callAgent())
    asyncio.run(callAgent())
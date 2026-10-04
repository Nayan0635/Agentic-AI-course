from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import asyncio
# # from mcp.client.session import ClientSession
# # from mcp.client.stdio import stdio_client,StdioServerParameters
from mcp import Client, StdioServerParameters
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
# Connect to MCP server
server = StdioServerParameters(
    command="python",
    args=["tools.py"]
)
async def callAgent():
    async with Client(server) as session:
        # Get all MCP tools
        tools = await session.list_tools()
        print("Available tools")
        # Convert MCP tools → OpenAI tools
        openai_tools = []
        for tool in tools.tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema # v2: snake_case, was inputSchema
                }
            })
            print(tool.name)
        while True:
            user_input = input("You: ")
            if user_input == "exit":
                print("Agent: Bye Bye")
                return
            # Connect to OpenAI
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "user", "content": user_input}
                ],
                tools=openai_tools
            )
            message = response.choices[0].message
            # Check whether AI called a tool
            if message.tool_calls:
                tool_call = message.tool_calls[0]
                toolName = tool_call.function.name
                toolArgs = json.loads(tool_call.function.arguments)
                # Call MCP tool
                result = await session.call_tool(
                    toolName,
                    arguments=toolArgs
                )
                print("Tool:", toolName)
                print("Agent:", result.content[0].text)
            else:
                print("Agent:", message.content)
if __name__ == "__main__":
    asyncio.run(callAgent())
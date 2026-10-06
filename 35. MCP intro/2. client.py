'''mcp v1 code'''
from mcp import Client,StdioServerParameters
import asyncio

#Connect to MCP Server
server = StdioServerParameters(
    command="python",
    args=['server.py']
)

async def callMCP():
    async with Client(server) as session:    
        #getting all tools from MCP server.
        tools = await session.list_tools()
        print("Available tools :")
        for tool in tools.tools:
            print(tool.name)
            print(tool.description)
            print(tool.inputSchema)
            #Calling the tool
            result =await session.call_tool(tool.name,{'a':20,'b':30})
            print("Result",result.content[0].text)

if __name__ == "__main__":
    asyncio.run(callMCP())
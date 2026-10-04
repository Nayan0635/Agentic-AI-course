from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client,StdioServerParameters
import asyncio

#Connect to MCP Server
server = StdioServerParameters(
    command="python",
    args=['server.py']
)

async def callMCP():
    async with stdio_client(server) as (read,write):
        async with ClientSession(read,write) as session:
            #initialize all tools.
            await session.initialize()
            #getting all tools from MCP server.
            tools = await session.list_tools()
            print("Available tools :")
            for tool in tools.tools:
                print(tool.name)
                print(tool.description)
                print(tool.inputSchema)
                # print(tool.input_schema)
                #Calling the tool
                result =await session.call_tool(tool.name,{'a':20,'b':30})
                print("Result",result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main=callMCP())
    # asyncio.run(callMCP())
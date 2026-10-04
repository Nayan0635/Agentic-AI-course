#loading the FastMCP class
# from mcp.server.fastmcp import FastMCP
from mcp.server.mcpserver import MCPServer

#Create an object of the FastMCP 
# mcp = FastMCP()
mcp = MCPServer()

#expose a tool using decorator
@mcp.tool()
def addNumbers(a:int,b:int)->int:
    '''addition of 2 numbers'''
    return a+b

#Running the server in background
if __name__ == "__main__":
    # print("MCP server is running")
    mcp.run()
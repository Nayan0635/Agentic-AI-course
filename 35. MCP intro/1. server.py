'''mcp v2 code'''

from mcp.server import MCPServer
mcp = MCPServer()

#expose a tool using decorator
@mcp.tool()
def addNumbers(a:int,b:int)->int:
    '''addition of 2 numbers'''
    return a+b

#Running the server in background
if __name__ == "__main__":
    mcp.run()
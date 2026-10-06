from mcp.server import MCPServer

mcp = MCPServer()
@mcp.tool()
def addNumbers(a:int,b:int)->str:
    '''addition of 2 numbers'''
    return f'Sum={(a+b)}'

@mcp.tool()
def multNumbers(a:int,b:int)->str:
    '''Multiplication of 2 numbers'''
    return f'Product={(a*b)}'
if __name__ =="__main__":
    mcp.run()
    
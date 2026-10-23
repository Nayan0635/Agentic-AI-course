from crewai.tools import tool

@tool
def addNumbers(a:int,b:int)->int:
    '''Addition of 2 numbers'''
    print("Addition Tool is called")
    return a+b
@tool
def multiNumbers(a:int,b:int)->int:
    '''multiplication or product of 2 numbers'''
    print("Multiply tool is called")
    return a*b

@tool
def saveFile(content:str)->str:
    '''saving file content to local file i.e hello.txt'''
    print("saveFile tool is called")
    with open("./hello.txt","w+") as file:
        file.write(content)
        file.close()
        return 'file created successfully'
    
@tool
def readFile()->str:
    '''reading content from created local file i.e hello.txt'''
    print("readFile tool is called")
    with open("./hello.txt","r+") as file:
        data = file.read()
        file.close()
        return data
    
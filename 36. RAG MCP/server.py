# MCP v2: FastMCP was renamed to MCPServer.
from mcp.server import MCPServer

from create_vector import embeddings

from langchain_community.vectorstores import FAISS



mcp = MCPServer("RAG+MCP server")
 

# Load FAISS Vector Store
vector_store = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)



@mcp.tool()
def search_pdf(question:str):
    """
      Search the EjobIndia PDF.

      You MUST use this tool when the user asks about:
        - EjobIndia
        - EjobIndia courses
        - EjobIndia placements
        - EjobIndia training
        - EjobIndia students
        - EjobIndia companies
        - Any information contained in the EjobIndia PDF.
    """
     
    docs =vector_store.similarity_search(
        query=question,
        k=2
    )

    context = "\n".join(doc.page_content for doc in docs)
    return context

if __name__=="__main__":
   
    mcp.run()

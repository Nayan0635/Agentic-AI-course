import os
from dotenv import load_dotenv
load_dotenv()

# Provider: "gemini" or "openai"
PROVIDER = "gemini"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBED_MODEL = {
    "gemini": "gemini-embedding-001",
    "openai": "text-embedding-3-small",
}[PROVIDER]

CHAT_MODEL = {
    "gemini": "gemini-3.1-flash-lite",
    "openai": "gpt-4.1-mini",
}[PROVIDER]

CHROMA_PATH = "./chromaDB"
COLLECTION_NAME = "documents"
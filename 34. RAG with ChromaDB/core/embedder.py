from google import genai
from openai import OpenAI
import config

_gemini = genai.Client(api_key=config.GEMINI_API_KEY) if config.PROVIDER == "gemini" else None
_openai = OpenAI(api_key=config.OPENAI_API_KEY) if config.PROVIDER == "openai" else None

def embed(text: str) -> list[float]:
    if config.PROVIDER == "gemini":
        resp = _gemini.models.embed_content(
            model=config.EMBED_MODEL, contents=text
        )
        return resp.embeddings[0].values
    else:
        resp = _openai.embeddings.create(
            model=config.EMBED_MODEL, input=text
        )
        return resp.data[0].embedding
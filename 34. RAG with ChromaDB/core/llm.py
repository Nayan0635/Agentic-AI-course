from google import genai
from openai import OpenAI
import config

_gemini = genai.Client(api_key=config.GEMINI_API_KEY) if config.PROVIDER == "gemini" else None
_openai = OpenAI(api_key=config.OPENAI_API_KEY) if config.PROVIDER == "openai" else None

def ask(context: str, question: str) -> str:
    prompt = f"""Context: {context}
Question: {question}
- Use the context above to answer.
- If the answer is not present, say "I don't know"."""

    if config.PROVIDER == "gemini":
        resp = _gemini.models.generate_content(
            model=config.CHAT_MODEL, contents=prompt
        )
        return resp.text
    else:
        resp = _openai.chat.completions.create(
            model=config.CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
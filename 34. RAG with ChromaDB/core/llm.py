from google import genai
from openai import OpenAI
import config

_gemini = genai.Client(api_key=config.GEMINI_API_KEY) if config.PROVIDER == "gemini" else None
_openai = OpenAI(api_key=config.OPENAI_API_KEY) if config.PROVIDER == "openai" else None


def ask(context: str, question: str) -> str:
    prompt = f"""You are answering questions using ONLY the context below.

    Context (each block is tagged with its source, e.g. [file.pdf § 3]): {context}
    Question: {question}

    Rules:
    - Answer using only the context above.
    - After each fact, cite the block(s) it came from using the same tag format: [file.pdf § 3].
    - If two files both contribute, cite both.
    - If the answer is not present in the context, say "I don't know".
    """

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
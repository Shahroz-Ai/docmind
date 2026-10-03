import os
import time
from dotenv import load_dotenv
from groq import Groq

from store import search

load_dotenv()
def get_api_key():
    """Read the key from .env locally, or from Streamlit secrets when deployed."""
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return None


client = Groq(api_key=get_api_key())

MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
]

SYSTEM_PROMPT = (
    "You are DocMind, an assistant that answers questions using only the "
    "provided context from a document. "
    "If the answer is not in the context, say that you could not find it "
    "in the document. Do not make things up. "
    "Keep the answer clear and concise, and mention page numbers like (Page 3)."
)


def build_context(hits):
    parts = []
    for h in hits:
        parts.append(f"[Page {h['page']}] {h['text']}")
    return "\n\n".join(parts)


def generate(question, hits, retries=2):
    context = build_context(hits)
    user_message = f"Context:\n{context}\n\nQuestion: {question}"

    for model in MODELS:
        for attempt in range(retries):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_message},
                    ],
                    temperature=0.2,
                )
                return response.choices[0].message.content
            except Exception as e:
                message = str(e)
                print(f"{model} attempt {attempt + 1} failed: {message[:80]}")
                # A missing or removed model will not recover, so skip it
                if "404" in message or "400" in message:
                    break
                time.sleep(2 * (attempt + 1))
    return "All models are busy right now. Please try again later."


def ask(question, k=4):
    hits = search(question, k=k)
    answer = generate(question, hits)
    return answer, hits


if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type 'exit'): ").strip()
        if question.lower() == "exit":
            break
        answer, hits = ask(question)
        print("\nAnswer:\n", answer)
        pages = sorted({h["page"] for h in hits})
        print("\nSources: pages", pages)
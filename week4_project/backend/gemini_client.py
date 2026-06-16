import os
from datetime import datetime

import requests


class GeminiClient:
    DEFAULT_TIMEOUT = 30
    DEFAULT_MAX_OUTPUT_TOKENS = 2048

    def __init__(
        self,
        api_key,
        model="gemini-3.5-flash",
        base_url="https://generativelanguage.googleapis.com",
        timeout=DEFAULT_TIMEOUT,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    @classmethod
    def from_env(cls):
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            return None
        timeout = os.getenv("GEMINI_TIMEOUT_SECONDS", str(cls.DEFAULT_TIMEOUT)).strip()
        try:
            timeout = float(timeout) if timeout else cls.DEFAULT_TIMEOUT
        except ValueError:
            timeout = cls.DEFAULT_TIMEOUT

        return cls(
            api_key=api_key,
            model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip() or "gemini-3.5-flash",
            timeout=timeout,
        )

    def current_date_text(self):
        return datetime.now().astimezone().strftime("%A, %B %d, %Y")

    def format_history(self, history, limit=10):
        if not history:
            return "No previous chat history."

        lines = []
        for message in history[-limit:]:
            role = message.get("role", "user")
            content = " ".join(str(message.get("content", "")).split())
            if content:
                lines.append(f"{role}: {content}")
        return "\n".join(lines) if lines else "No previous chat history."

    def build_instruction_block(self, history=None, current_date=None):
        date_text = current_date or self.current_date_text()
        return f"""
You are Bnk Chatbot.
Current date: {date_text}
Use the current date above for all date/time questions. Do not guess another date.
Use chat history to understand follow-up questions and pronouns.
Answer in the same language as the user.
Give a useful answer with enough detail; do not be overly terse.

Chat history:
{self.format_history(history)}
""".strip()

    def generate_answer(self, question, contexts, history=None, current_date=None):
        context_text = "\n\n".join(
            f"Source: {context['chunk_id']}\n{context['text']}"
            for context in contexts
        )
        prompt = f"""
{self.build_instruction_block(history=history, current_date=current_date)}

Use only the provided context to answer the question.
If the answer is not in the context, say: I do not know from the provided context.
Include source ids naturally when useful.

Context:
{context_text}

Question:
{question}
""".strip()

        return self.generate_text(prompt)

    def generate_general_answer(self, question, history=None, current_date=None):
        prompt = f"""
{self.build_instruction_block(history=history, current_date=current_date)}

Answer the user question normally.

Question:
{question}
""".strip()
        return self.generate_text(prompt)

    def generate_text(self, prompt):
        url = f"{self.base_url}/v1beta/models/{self.model}:generateContent"
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,
            },
            json={
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}],
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": self.DEFAULT_MAX_OUTPUT_TOKENS,
                },
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        parts = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [])
        )
        text = "".join(part.get("text", "") for part in parts).strip()

        if not text:
            raise RuntimeError("Gemini returned an empty response")

        return text

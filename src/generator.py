
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


class Generator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY missing from .env")

        self.client = genai.Client(api_key=api_key)

    def generate(self, query, context):
        prompt = f"""
            You are ContextThread, a technical research assistant.

            Answer the user's question using ONLY the supplied evidence.

            Rules:
            - If the evidence is insufficient, say so clearly.
            - Do not invent facts or citations.
            - Cite supporting evidence using [SOURCE 1], [SOURCE 2], etc.
            - Distinguish evidence from inference.
            - Be precise and concise.

            EVIDENCE:
            {context}

            QUESTION:
            {query}

            Write a grounded answer with citations.
            """

        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text
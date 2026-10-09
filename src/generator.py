
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()


class Generator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY missing from .env"
            )

        self.client = genai.Client(api_key=api_key)

    def generate(self, query, context):
        prompt = f"""
You are ContextThread, a technical research assistant.

Answer using ONLY the supplied evidence.
If evidence is insufficient, say so clearly.
Do not invent facts or citations.
Cite supporting evidence using [SOURCE 1], [SOURCE 2], etc.

EVIDENCE:
{context}

QUESTION:
{query}

Write a grounded answer with citations.
"""

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                if not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return response.text

            except errors.ServerError:
                if attempt == 2:
                    raise

                time.sleep(2 ** attempt)

        raise RuntimeError("Generation failed.")

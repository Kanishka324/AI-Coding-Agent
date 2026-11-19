
import os
import time

from groq import Groq
from dotenv import load_dotenv

from llm.prompts import CODING_AGENT_SYSTEM_PROMPT

load_dotenv()


class GroqClient:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is missing from .env"
            )

        self.client = Groq(api_key=api_key)

        self.model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
        )

        self.max_retries = 3
        self.retry_delay = 2

    def _convert_tools(self, tool_declarations):
        """Convert registry tools to Groq function format."""

        groq_tools = []

        for tool in tool_declarations:

            groq_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            })

        return groq_tools

    def get_response(self, messages, tool_declarations):

        tools = self._convert_tools(tool_declarations)

        for attempt in range(self.max_retries + 1):

            try:

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    parallel_tool_calls=False
                )

                return response

            except Exception as error:

                status_code = getattr(
                    error,
                    "status_code",
                    None
                )

                retryable_codes = {
                    429, 500, 502, 503, 504
                }

                if status_code not in retryable_codes:
                    raise

                if attempt == self.max_retries:
                    raise

                delay = self.retry_delay * (2 ** attempt)

                print(
                    f"\nGroq API temporarily unavailable."
                    f"\nRetrying in {delay} seconds..."
                    f"\nAttempt {attempt + 1} of "
                    f"{self.max_retries}"
                )

                time.sleep(delay)

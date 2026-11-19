
import os
import time

from google import genai
from dotenv import load_dotenv

from llm.prompts import CODING_AGENT_SYSTEM_PROMPT

load_dotenv()


class GeminiClient:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing from .env"
            )

        self.client = genai.Client(api_key=api_key)

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        # Retry configuration
        self.max_retries = 3
        self.retry_delay = 2

        # Temporary API errors
        self.retryable_errors = {
            429,
            500,
            502,
            503,
            504
        }

    def _is_retryable_error(self, error):

        error_code = getattr(error, "code", None)

        if error_code in self.retryable_errors:
            return True

        error_message = str(error).lower()

        retryable_messages = [
            "service_unavailable",
            "high demand",
            "resource_exhausted",
            "too many requests",
            "internal server error",
            "deadline exceeded"
        ]

        return any(
            message in error_message
            for message in retryable_messages
        )

    def _create_interaction(self, **kwargs):

        for attempt in range(self.max_retries + 1):

            try:

                return self.client.interactions.create(
                    **kwargs
                )

            except Exception as error:

                if not self._is_retryable_error(error):
                    raise

                if attempt == self.max_retries:
                    print(
                        "\nGemini API is still unavailable "
                        "after all retry attempts."
                    )
                    raise

                delay = self.retry_delay * (2 ** attempt)

                print(
                    f"\nGemini API temporarily unavailable."
                    f"\nRetrying in {delay} seconds..."
                    f"\nAttempt {attempt + 1} of "
                    f"{self.max_retries}"
                )

                time.sleep(delay)

    def start_interaction(
        self,
        user_prompt,
        tool_declarations
    ):

        interaction = self._create_interaction(
            model=self.model,
            system_instruction=CODING_AGENT_SYSTEM_PROMPT,
            input=user_prompt,
            tools=tool_declarations
        )

        return interaction

    def continue_interaction(
        self,
        interaction_id,
        tool_results,
        tool_declarations
    ):

        interaction = self._create_interaction(
            model=self.model,
            previous_interaction_id=interaction_id,
            system_instruction=CODING_AGENT_SYSTEM_PROMPT,
            input=tool_results,
            tools=tool_declarations
        )

        return interaction

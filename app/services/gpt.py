import json
from openai import AsyncOpenAI
from config import config
from app.utils.logger import logger

# THE BRAIN CONNECTOR: The bridge between SQL and Silicon.
# Rules strictly followed: Async, JSON-enforced, Error-resilient.

class GPTService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.openai_api_key)
        self.model = "gpt-4o-mini"

    async def health_check(self) -> bool:
        """
        PULSE CHECK: Verifies OpenAI connectivity with a 1-token request.
        Rule 7: Expect Failure. If this fails, we enter 'Limp Mode'.
        """
        if not config.openai_api_key:
            logger.warning("GPT Service: No API Key provided.")
            return False
            
        try:
            # The cheapest possible request: Just 1 token.
            await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=1
            )
            return True
        except Exception as e:
            logger.error(f"GPT Pulse Failure: {e}")
            return False

    async def summarize_idea(self, raw_text: str) -> dict:
        """
        Takes raw text and returns a structured JSON summary.
        Refinement: Uses JSON-mode to ensure the output is machine-readable.
        """
        system_prompt = (
            "You are Mr. Assistant's Brain. Your job is to take raw 'ideas' and turn them into structured data. "
            "Return a JSON object with the following keys: "
            "'summary' (1 sentence), 'action_points' (list of 3 items), 'category' (e.g. Work, Life, Tech)."
        )
        
        try:
            logger.info("GPT: Summarizing new inspiration...")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Summarize this idea: {raw_text}"}
                ],
                response_format={"type": "json_object"}
            )
            
            # Extract and parse the content
            content = response.choices[0].message.content
            logger.info("GPT: Successfully extracted structured data.")
            return json.loads(content)

        except Exception as e:
            logger.error(f"GPT Error: Failed to summarize idea: {e}", exc_info=True)
            # Safe Fallback: Rule 14 (Zero Downtime)
            return {
                "summary": "Summary temporarily unavailable.",
                "action_points": ["Review later in the vault."],
                "category": "Uncategorized"
            }

# Global singleton for easy importing
gpt_service = GPTService()

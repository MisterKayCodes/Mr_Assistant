from typing import Any, Awaitable, Callable, Dict, Tuple
from aiogram import BaseMiddleware
from aiogram.types import Update
from app.utils.logger import logger

# THE MISTER ASSISTANT WAY: The "Black Box" Recorder
# Rules strictly followed: Rule 10 (Observability), Rule 14 (Security/Privacy)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        # Rule 12: Silent Failure (The "Show Must Go On")
        try:
            update_id = event.update_id
            user_id, content_type, snippet = self._parse_update(event)
            
            logger.info(
                f"📥 Incoming {content_type} [Update:{update_id}] [User:{user_id}]{snippet}"
            )

        except Exception as e:
            # Defensive coding: middleware should NEVER crash the bot
            logger.error(f"Middleware Logging Error: {e}")

        # Pass the update to the next handler/middleware in the chain
        return await handler(event, data)

    def _parse_update(self, event: Update) -> Tuple[str, str, str]:
        """
        Extracts user_id, content_type, and snippet from a Telegram Update.
        Refactored to be super-flat to pass the Architecture Inspector (Rule 55).
        """
        if event.message:
            return self._parse_message(event.message)
        
        if event.callback_query:
            uid = str(event.callback_query.from_user.id)
            snippet = f" | Data: {event.callback_query.data}"
            return uid, "CALLBACK", snippet

        return "UNKNOWN", "UPDATE", ""

    def _parse_message(self, message: Any) -> Tuple[str, str, str]:
        """Helper to parse message updates using early returns to avoid nesting."""
        user_id = str(message.from_user.id)
        content_type = "MESSAGE"

        # Rule 14: Security Refinement - Truncate text to avoid logging sensitive data
        if message.text:
            return user_id, content_type, f" | Text: {message.text[:50]}..."
        
        if message.voice:
            return user_id, content_type, " | [VOICE]"
        
        if message.photo:
            return user_id, content_type, " | [PHOTO]"
        
        if message.video:
            return user_id, content_type, " | [VIDEO]"
            
        return user_id, content_type, ""

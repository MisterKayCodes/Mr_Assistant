from typing import Any, Awaitable, Callable, Dict
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
            # Prepare metadata for logging
            update_id = event.update_id
            user_id = "UNKNOWN"
            content_type = "UPDATE"
            snippet = ""

            if event.message:
                user_id = event.message.from_user.id
                content_type = "MESSAGE"
                # Rule 14: Security Refinement - Truncate text to avoid logging sensitive data
                if event.message.text:
                    snippet = f" | Text: {event.message.text[:50]}..."
                elif event.message.voice:
                    snippet = " | [VOICE]"
                elif event.message.photo:
                    snippet = " | [PHOTO]"
            
            elif event.callback_query:
                user_id = event.callback_query.from_user.id
                content_type = "CALLBACK"
                snippet = f" | Data: {event.callback_query.data}"

            logger.info(
                f"📥 Incoming {content_type} [Update:{update_id}] [User:{user_id}]{snippet}"
            )

        except Exception as e:
            # Defensive coding: middleware should NEVER crash the bot
            logger.error(f"Middleware Logging Error: {e}")

        # Pass the update to the next handler/middleware in the chain
        return await handler(event, data)

from sqlalchemy import select
from app.data.database import async_session_maker
from app.data.models import Message, MessageType

# THE MISTER ASSISTANT WAY: The "Waiter" who handles the mess.
# Rules strictly followed: Async, DAL/Repository pattern, error handling.

async def save_message(user_id: int, raw_text: str, msg_type: MessageType = MessageType.TEXT) -> bool:
    """
    Saves a message to the 'Memory' layer.
    Returns True if successful, False otherwise.
    Note: We use the Enum for msg_type to prevent typos!
    """
    async with async_session_maker() as session:
        try:
            new_msg = Message(
                user_id=user_id,
                raw_text=raw_text,
                type=msg_type.value # Store the raw string value in DB
            )
            session.add(new_msg)
            await session.commit()
            return True
        except Exception as e:
            # Rule 10: Observability. We log the error but don't crash the bot.
            print(f"[!] Database Error in save_message: {e}")
            await session.rollback()
            return False

async def get_recent_messages(user_id: int, limit: int = 10) -> list[dict]:
    """
    Fetches recent history for a user.
    Returns a list of dictionaries (The "Waiter" brings the food, not the stove!).
    """
    async with async_session_maker() as session:
        try:
            query = (
                select(Message)
                .where(Message.user_id == user_id)
                .order_by(Message.timestamp.desc())
                .limit(limit)
            )
            result = await session.execute(query)
            messages = result.scalars().all()
            
            # Convert SQLAlchemy objects to simple dictionaries immediately.
            # This prevents "DetachedInstanceError" in other layers.
            return [
                {
                    "id": m.id,
                    "timestamp": m.timestamp,
                    "user_id": m.user_id,
                    "raw_text": m.raw_text,
                    "summary": m.summary,
                    "type": m.type
                }
                for m in messages
            ]
        except Exception as e:
            print(f"[!] Database Error in get_recent_messages: {e}")
            return []

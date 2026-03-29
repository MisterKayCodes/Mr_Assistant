from aiogram import Router, types, F
from app.core.logic import analyze_message
from app.data.repository import save_message
from app.utils.logger import logger

router = Router(name="message_handlers")

@router.message(F.text & ~F.text.startswith("/"))
async def handle_text_message(message: types.Message):
    """
    The Mouth: Receives Telegram message.
    1. Sends to Brain (logic.py) for analysis.
    2. Sends to Memory (repository.py) for storage.
    3. Provides feedback Loop.
    """
    user_id = message.from_user.id
    raw_text = message.text
    
    # Brain Analysis (Translation Layer)
    processed = analyze_message(user_id=user_id, text=raw_text)
    
    # Memory Storage (Repository)
    success = await save_message(
                        user_id=user_id, 
                        raw_text=raw_text, 
                        msg_type=processed.msg_type
                    )
    
    if not success:
        # Rule 12 & 14: Silently handle DB failure for better UX, but log it.
        await message.answer("⚠️ Sorry, I had a momentary lapse in memory. (DB Error logged)")
        return

    # Feedback Loop (Refinement: Vocal Feedback)
    if processed.is_idea:
        await message.answer("Idea logged to the vault 💡")
    else:
        # For standard text, we use a simple acknowledgment emoji
        # In AioGram 3.x, if the bot has permission, we could use message.react() 
        # But for reliability, we'll use a simple text response for now.
        await message.answer("Saved ✅")
        
    logger.info(f"Successfully processed {processed.msg_type} for user {user_id}")

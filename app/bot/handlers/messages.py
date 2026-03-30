from aiogram import Router, types, F, Bot
from app.core.logic import analyze_message
from app.data.repository import save_message
from app.services.gpt import gpt_service
from app.utils.logger import logger
import asyncio

# THE MOUTH: The communication layer of Mr. Assistant.
# Rules strictly followed: UX feedback, Error-resilience, Confirmation loops.

router = Router(name="message_handlers")

@router.message(F.text & ~F.text.startswith("/"))
async def handle_text_message(message: types.Message, bot: Bot):
    """
    Receives Telegram message.
    1. Analyzes (Brain)
    2. Summarizes (GPT) - ONLY IF IDEA
    3. Stores (Memory)
    4. Feedback (UX)
    """
    user_id = message.from_user.id
    raw_text = message.text
    
    # 1. Brain Analysis (Classification)
    processed = analyze_message(user_id=user_id, text=raw_text)
    
    summary_data = None
    
    # 2. GPT Augmentation (The "Thinking" UI)
    if processed.is_idea:
        # UX: Show the "Thinking" state immediately
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        # Call the Silicon Brain
        summary_data = await gpt_service.summarize_idea(raw_text)
        
    # 3. Memory Storage (Self-Healing Fallback included in save_message)
    success = await save_message(
                        user_id=user_id, 
                        raw_text=raw_text, 
                        msg_type=processed.msg_type,
                        summary=summary_data
                    )
    
    if not success:
        await message.answer("⚠️ Memory failure. The raw idea is logged, but storage failed.")
        return

    # 4. The Confirmation Loop (Rule: Feedback to User)
    if processed.is_idea and summary_data:
        # Compact summary for the user
        response = (
            f"🎯 **IDEA CAPTURED**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📝 **Summary:** {summary_data.get('summary')}\n"
            f"📂 **Category:** {summary_data.get('category')}\n"
            f"✅ **Next Steps:**\n"
            + "\n".join([f"• {item}" for item in summary_data.get('action_points', [])])
        )
        await message.answer(response, parse_mode="Markdown")
    else:
        # Standard text acknowledgment
        await message.answer("Stored [OK]")
        
    logger.info(f"Processed {processed.msg_type} for user {user_id}")

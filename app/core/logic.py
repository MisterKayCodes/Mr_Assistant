from app.core.schemas import ProcessedMessage, MessageType
from app.utils.logger import logger

def analyze_message(user_id: int, text: str) -> ProcessedMessage:
    """
    The Brain: Pure logic and text parsing.
    Decides if a message is an idea or a standard text message.
    """
    is_idea = False
    msg_type = MessageType.TEXT
    
    # Logic: Detect #idea tag or /idea command prefix
    clean_text = text.strip()
    if "#idea" in clean_text.lower():
        is_idea = True
        msg_type = MessageType.IDEA
        logger.info(f"Brain detected an IDEA from user {user_id}")
    elif clean_text.lower().startswith("/idea"):
        is_idea = True
        msg_type = MessageType.IDEA
        # Note: We keep the '/idea' prefix for now as it's part of the raw_text
        logger.info(f"Brain detected an IDEA command from user {user_id}")
    else:
        logger.debug(f"Brain processing standard text from user {user_id}")

    return ProcessedMessage(
        user_id=user_id,
        raw_text=clean_text,
        msg_type=msg_type,
        is_idea=is_idea
    )

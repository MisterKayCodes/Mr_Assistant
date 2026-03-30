import re
from app.core.schemas import ProcessedMessage, MessageType
from app.utils.logger import logger

def analyze_message(user_id: int, text: str) -> ProcessedMessage:
    """
    The Brain: Pure logic and text parsing.
    Decides if a message is an idea or a standard text message.
    Refinement: Uses Regex for foolproof detection (Rule 11).
    """
    is_idea = False
    msg_type = MessageType.TEXT
    
    clean_text = text.strip()
    
    # SENIOR REFINE: Use regex to ensure we only match #idea as a whole word.
    # (?i) = case insensitive, \b = word boundary.
    # This prevents matching #ideal, #ideology, etc.
    if re.search(r"(?i)#idea\b", clean_text):
        is_idea = True
        msg_type = MessageType.IDEA
        logger.info(f"Brain detected an IDEA via hashtag from user {user_id}")
    elif clean_text.lower().startswith("/idea"):
        is_idea = True
        msg_type = MessageType.IDEA
        logger.info(f"Brain detected an IDEA via command from user {user_id}")
    else:
        logger.debug(f"Brain processing standard text from user {user_id}")

    return ProcessedMessage(
        user_id=user_id,
        raw_text=clean_text,
        msg_type=msg_type,
        is_idea=is_idea
    )

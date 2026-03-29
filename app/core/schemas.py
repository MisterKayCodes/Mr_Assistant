from pydantic import BaseModel
from typing import Optional
from enum import Enum

class MessageType(str, Enum):
    """
    Standardizing the types of messages we handle.
    """
    TEXT = "text"
    VOICE = "voice"
    IDEA = "idea"

class ProcessedMessage(BaseModel):
    """
    The Translation Layer: Converts messy Telegram data into 
    clean, structured data for the Memory.
    """
    raw_text: str
    msg_type: MessageType
    is_idea: bool = False
    user_id: int

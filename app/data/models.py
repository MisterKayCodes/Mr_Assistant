from datetime import datetime
from enum import Enum
from typing import Optional, Any
from app.core.schemas import MessageType
from sqlalchemy import BigInteger, String, JSON, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # The UTC timestamp is crucial for accurate /weekly reports across timezones
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # THE SENIOR FIX: The BigInteger! 
    # Prevents the 32-bit crash when Telegram issues huge IDs
    user_id: Mapped[int] = mapped_column(BigInteger)
    
    raw_text: Mapped[str] = mapped_column(String)
    
    # Summary is JSON, nullable because Phase 1 doesn't have GPT yet
    summary: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # The Guardrail: Storing our strict Enum value. 
    type: Mapped[str] = mapped_column(String, default=MessageType.TEXT.value)

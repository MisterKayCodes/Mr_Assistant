from aiogram import Router
from .base import router as base_router
from .messages import router as messages_router

# The Senior Router Pattern: One single point of entry for main.py
# This keeps main.py from becoming "Spaghetti Code" as we grow.

router = Router(name="main_router")

# Order matters: base handlers (commands) first, then catch-all messages.
router.include_router(base_router)
router.include_router(messages_router)

from aiogram import Router, types
from aiogram.filters import CommandStart, Command

router = Router(name="base_handlers")

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Handle /start command.
    """
    welcome_text = (
        "**Welcome to Mr. Assistant!**\n\n"
        "I am your digital second brain. Send me ideas, thoughts, or voice "
        "memos, and I'll keep them safe for you.\n\n"
        "**Core Skills:**\n"
        "[IDEA] Tag ideas with `#idea` to log them to the vault.\n"
        "[VOICE] Send voice messages for automatic transcription (coming soon).\n"
        "[STATS] Get a `/weekly` summary of your thoughts (coming soon).\n\n"
        "Let's build something great."
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """
    Handle /help command.
    """
    help_text = (
        "**Mr. Assistant Help**\n\n"
        "Current Commands:\n"
        "/start - Restart and see welcome info.\n"
        "/help - See this message.\n\n"
        "Usage:\n"
        "- Just send any text to save it.\n"
        "- Include `#idea` in your text to mark it as an idea.\n"
    )
    await message.answer(help_text, parse_mode="Markdown")

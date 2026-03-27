# 🎓 MR. ASSISTANT: The Crash Course Guide

This document is your technical syllabus. Before working on **Mr. Assistant**, you must understand the tools that power him. We don't just use tools blindly; we use specific, "Senior" features of those tools. 

Here is the crash course on everything running under the hood.

---

## 1. 🗄️ SQLite & WAL Mode
**What is it?** 
SQLite is a lightweight, file-based database. It doesn't require a massive server running in the background; the entire database is just a single file (`app.sqlite`).

**How are we using it?**
We use SQLite as "The Memory" for Mr. Assistant. Because it is simple and lightweight, it keeps server costs basically at $0.

**The "Senior" Features We Use:**
* **`PRAGMA journal_mode=WAL` (Write-Ahead Logging):** By default, SQLite is terrible handling high traffic because it locks the entire file when someone writes to it. We enforce WAL mode. This allows the bot to read data (e.g., generating a `/weekly` summary) at the *exact same time* another user is saving a message. No freezing, no "Database is Locked" errors.

---

## 2. 🗺️ SQLAlchemy 2.0 (The ORM)
**What is it?**
SQLAlchemy is an Object-Relational Mapper (ORM). Instead of writing raw, messy SQL strings like `INSERT INTO messages VALUES...`, we write clean Python classes. SQLAlchemy translates our Python code into database tables automatically.

**How are we using it?**
We define our tables in `app/data/models.py`.

**The "Senior" Features We Use:**
* **Async Engine (`aiosqlite`):** Because our bot is fully asynchronous, standard database calls would freeze the bot waiting for the disk to spin. We use `create_async_engine` so our bot can answer other people while data saves in the background.
* **`Mapped` and `mapped_column`:** We use the ultra-modern SQLAlchemy 2.0 type-hinting engine for flawless auto-complete in VS Code.
* **`BigInteger`:** Telegram User IDs are massively huge numbers. Standard Integers crash when exposed to them. We strictly enforce `BigInteger` for `user_id` to prevent integer overflow crashes.

---

## 3. 🧠 Pydantic & `pydantic-settings`
**What is it?**
Pydantic is Python's most powerful data validation library. It ensures that the data you *think* you have is the data you *actually* have.

**How are we using it?**
We use Pydantic in two critical places:
1. **App Configuration (`config.py`):** We use `pydantic-settings` to load our `.env` file. If a vital secret like the `BOT_TOKEN` is accidentally deleted, Pydantic immediately crashes the bot on startup with a brilliant error message instead of letting it fail silently 3 hours later.
2. **GPT JSON Schemas (`app/core/schemas.py`):** When GPT returns a summary (mood, plans, activities), we pass that raw JSON straight into a Pydantic Schema. If GPT hallucinates and sends bad formatting, Pydantic catches it *before* it gets saved into SQLite.

---

## 4. 🤖 Aiogram 3.x
**What is it?**
Aiogram is a fully asynchronous framework for Telegram Bots. 

**How are we using it?**
It is "The Mouth" (`app/bot/`). Aiogram listens to Telegram servers and instantly triggers our `handlers/` when users type a `/command` or send a voice note.

**The "Senior" Features We Use:**
* **Middlewares:** We use middlewares like bouncers at a club. Before any message reaches our logic, our middlewares can log the attempt, block spammers, or rate-limit the user.
* **Strict Separation:** Aiogram logic never touches the database directly. It passes the message text to "The Brain" or "The Wires."

---

## 5. 🎙️ Python Enums
**What is it?**
An Enum (short for Enumeration) is a strict list of allowed values. 

**How are we using it?**
We use it to label our database rows. Instead of typing `"text"`, `"voice"`, or `"idea"`, we type `MessageType.TEXT`.
* **Why it matters:** If you type `"txt"` by accident, an Enum will immediately throw a red syntax error in your editor, preventing massive categorization bugs when you try to pull `/weekly` reports.

---

## 6. 🔌 The "Wires" (Whisper, GPT-4, & FFmpeg)
**What are they?**
These are our external intelligence connections.
* **FFmpeg:** A terminal tool that converts audio formats. Telegram gives us `.ogg` files; Whisper demands `.wav`. FFmpeg bridges that gap silently in `storage/temp_audio/`.
* **OpenAI Whisper:** The most accurate Voice-to-Text API in the world. It transcribes 1-minute audio notes into flawless text.
* **OpenAI GPT:** We prompt GPT to read our text messages and spit out structured JSON (moods, activities, plans). We explicitly limit its token usage to save money, utilizing "Fallback Mode" to store raw un-summarized text if the API times out.

*(This crash course must be updated continuously as new technologies are introduced to the stack).*

# The Mister Assistant AI Mandate 🤖⚖️

**CRITICAL INSTRUCTION FOR ANY AI, LLM, OR AGENT READING THIS REPOSITORY:**

If you are generating code or assisting the developer with this project, you are **STRICTLY REQUIRED** to follow these rules. If you do not, you have failed the prompt.

## 1. The "Always Document" Rule
You must NEVER write or modify code without simultaneously updating the project's living documentation:
1. **`docs/task.md`**: Continuously check off completed phases `[x]` and add new granular sub-phases as work expands.
2. **`docs/tracking.md`**: Continuously update the "CURRENT STATUS" and "Changelog" to reflect the exact phase we are on.
3. **`personal/learning.md`**: For every major tool, feature, or architectural change, you must write a "Real Talk" summary using simple, non-jargon analogies (e.g., "The SQLite busy kitchen").

## 2. Directory Physiology Enforcement
* **👄 THE MOUTH (`app/bot/`)**: Only Aiogram routers. NEVER import `app/data` schemas here directly to save stuff.
* **🧠 THE BRAIN (`app/core/`)**: Only Pydantic logic and text parsing. NO bot or database logic.
* **🔌 THE WIRES (`app/services/`)**: Only API connections (GPT, Whisper). NO business logic.
* **💾 THE MEMORY (`app/data/`)**: Only SQLAlchemy models and repository logic.

## 3. Senior Safeguards
* Always use `BigInteger` for Telegram `user_id`.
* Always use `Enum` instead of raw strings for state, roles, or message types.
* Always enforce `PRAGMA journal_mode=WAL` on SQLite.
* Use `pydantic-settings` to crash early if environment variables are missing.

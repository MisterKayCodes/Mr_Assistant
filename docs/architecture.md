# Rules for the Inspector & The AI

## 1. The "Continuous Documentation" Rule
The AI Assistant MUST NEVER write code without simultaneously updating the project's vital documentation. 
* **`docs/task.md`**: Must be updated continuously. Check off `[x]` for completed tasks, and add new sub-phases `[ ]` dynamically as work scales.
* **`personal/learning.md`**: Must be updated with "Real Talk" analogies for every major architectural decision (e.g., WAL mode, Enums, BigInteger). 

## 2. Directory Separation Rules
* **The Brain (`app/core/`)**: This zone contains pure logic, Pydantic schemas, and formatters. It cannot import database models or bot routers.
* **The Memory (`app/data/`)**: This zone contains SQLAlchemy models and engine setup. It cannot import bot logic or external APIs.
* **The Mouth (`app/bot/`)**: This zone contains the Telegram connection (Aiogram routers and middlewares). 
* **The Wires (`app/services/`)**: External API modules (GPT, Whisper).

## 3. SQLite Concurrency (WAL Mode)
Any connection to SQLite MUST explicitly enforce `PRAGMA journal_mode=WAL` to prevent the bot from throwing `Database is Locked` errors during high concurrency async operations.

## 4. Typos and Type Enforcement
Never use raw strings (`"text"`, `"voice"`) for data state. Always define Python `Enum` classes to establish unbreakable guardrails. Telegram `user_id` fields must always be `BigInteger` to prevent overflow crashes.

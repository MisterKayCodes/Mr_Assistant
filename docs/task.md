# MR. ASSISTANT MVP Task List

## Setup & Planning
- [x] Create project directory structure matching Mister Starter Pack
- [x] Write implementation plan for Phase 1
- [x] Review and approve Phase 1 plan

## Phase 1 (Day 1): Base Telegram Bot & Database
- [x] Phase 1.0: Environment & Config (`requirements.txt`, `.env`, `config.py`)
- [x] Phase 1.1: Database Engine (`app/data/database.py` with WAL mode)
- [x] Phase 1.1: Database Models (`app/data/models.py` with BigInteger and Enum)
- [x] Phase 1.2: Repository Layer (`app/data/repository.py`)
- [ ] Phase 1.3: Digital Constitution (`scripts/dev_constitution.py`)
- [ ] Phase 1.4: Middleware (`app/bot/middlewares/__init__.py` for logging)
- [ ] Phase 1.5: Handlers (`app/bot/handlers/base.py`, `app/bot/handlers/messages.py`)
- [ ] Phase 1.6: Bot Entry Point (`app/bot/main.py`)

## Phase 2 (Day 2): Text Summarization
- [ ] GPT API integration for text summarization
- [ ] Update DB schema for JSON summary
- [ ] Store summary in DB

## Phase 3 (Day 3): Weekly Report
- [ ] Implement `/weekly` command
- [ ] GPT prompt for weekly summary
- [ ] Fetch past 7 days data

## Phase 4 (Day 4): Voice Messages
- [ ] Voice download via telegram
- [ ] FFmpeg conversion
- [ ] Whisper API integration
- [ ] GPT summary of transcription

## Phase 5 (Day 5): Idea Dump
- [ ] Identify `#idea` or `/ideas`
- [ ] Store ideas separately or tagged
- [ ] Implement `/ideas` retrieval

## Phase 6 (Day 6): Hardening & Error Handling
- [ ] Implement fallbacks and retries
- [ ] Add logging
- [ ] Token tracking and limits

## Phase 7 (Day 7): Testing & Optimization
- [ ] Edge cases testing
- [ ] Final polishing

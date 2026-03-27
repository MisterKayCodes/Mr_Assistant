# Mister Assistant: Software Development Lifecycle (SDLC) Architecture

This repository defines the Mister Assistant SDLC protocol. It provides a restrictive, highly opinionated framework for building scalable, modular Python projects (APIs, Bots, and Scrapers). By enforcing structural discipline and automated checks at runtime, the architecture prevents the accumulation of technical debt, tight coupling, and "spaghetti code."

---

## 1. Project Initialization & Environment Setup

### Structural Generation
To initiate a new project, modify `tree_structure.txt` to reflect your specific domain needs and execute:

```bash
python tree_generator.py
```

This enforces a standardized directory layout before any code is written.

### Environment Bootstrapping
Execute `setup.bat`. This process:
1. Provisions the Python virtual environment (`venv`).
2. Installs required dependencies defined in `requirements.txt`.

### Execution and Hot-Reload Pipeline
Launch the system via `run.bat`. This entry point performs several critical operations:
- Automatically validates dependency hashes and installs updates if `requirements.txt` is altered.
- Identifies and terminates orphaned ("ghost") Python processes to prevent port contention.
- Executes the **Architecture Inspector** to validate codebase integrity.
- Boots the application (`main.py`) using `watchfiles` to enable continuous hot-reloading during development.
- Surfaces mandatory prompts reminding developers to update architectural documentation.

---

## 2. Core Architecture: The Layered Domain Model

The codebase is strictly segregated into independent layers. Cross-contamination between layers will cause the Architecture Inspector to block execution.

- **`app/bot/` (The Interface):** Manages user interaction and UI elements (e.g., Telegram handlers, CLI inputs).
- **`app/schemas/` (The Translation Layer):** Pydantic models and dataclasses. The Interface layer must convert external payloads into these standardized schemas before communicating with Core logic.
- **`app/core/` (The Business Logic):** Pure, platform-agnostic business logic. This layer defines system states (via internal FSMs) and executes transformations. **Constraint:** No UI, internet, or database dependencies may be imported here.
- **`app/services/` (The Integration Layer):** The exclusive domain for external API integration and network requests.
- **`app/data/` (The Persistence Layer):** Manages database connections, ORMs, and file persistence.
- **`app/utils/` (Shared Modules):** Provides cross-cutting concerns like standardized logging.

---

## 3. Automated Code Enforcement

Manual code review is insufficient for structural integrity. The `scripts/architecture_inspector.py` enforces the following constraints automatically:

### 3.1. Cyclomatic Complexity Monitoring
Deep architectural nesting heavily impairs debuggability. The visual AST inspector monitors control flow statements (`if`, `for`, `while`, `try`). Code nesting exceeding three levels triggers a "Spaghetti Warning" and halts execution.

### 3.2. Payload Length Restrictions (The 200-Line Rule)
Files exceeding 200 lines indicate poorly factored logic and represent immediate technical debt. Refactoring is required.

### 3.3. Layer Isolation Enforcement
The Inspector statically analyzes abstract syntax trees for prohibited imports. For instance, `app/core/` possessing an import referencing `aiogram` or `sqlalchemy` is an immediate fatal exception.

---

## 4. Security & Synchronization (Git Hook Automations)

The repository integrates a pre-push synchronization tool: `scripts/git_sync.py`.

### Automated Secret Scanning
Prior to committing, the script performs a pattern-matching scan across the directory tree. If exposed `.env` files, hardcoded `API_KEY` assignments, OpenAI tokens (`sk-...`), or Telegram bot tokens are detected in source files, the synchronization is critically aborted to prevent credential leakage.

### Session Tracking Protocol
Direct `git push` commands are deprecated. Feature updates and refactors must be logged within `docs/tracking.md`. A new entry in this tracker acts as the commit message payload, triggering `git_sync.py` to stage, commit, and push modifications upstream.

---

## 5. Required Documentation Standards (The Librarian Protocols)

Any human developer or AI agent modifying this project must adhere to strict documentation protocols:

1. **The Tracking Manifest (`docs/tracking.md`):** Logs the operational history (the *what* and *when*). Appending entries here acts as the project's continuous integration trigger.
2. **The Decision Log (`docs/tracking.md`):** Records major architectural trade-offs. (e.g., "Decision: Adopted SQLite over PostgreSQL. Rationale: Minimized external orchestration dependencies during MVP phase.") 
3. **The Learning Ledger (`personal/learning.md`):** Documents the *how* and *why* of complex engineering fixes for future retrieval.
4. **The Context Architecture Map (`scripts/project_map.py`):** Execute this script to generate `project_map.txt`. This map outputs the current folder tree and all function docstrings, serving as an optimal context window initialization for AI-assisted development.
5. **Testing Subsystem (`tests/` and `testme/`):** Do not validate business logic by manually interacting with the UI. Isolate and validate logic using discrete test scripts to deduce failures rapidly.

---

## 6. AI Agent Ignition Sequence

If you are an AI Autonomous Agent reading this document to initiate development, you are strictly bound by the rules above. Before generating any application code, you must execute the following sequence:

1. **Map Context:** Run `python scripts/project_map.py`. This provides a complete structural map of the execution environment.
2. **Read History:** Review `docs/tracking.md` and `personal/learning.md` to internalize domain context and previous architectural decisions.
3. **Acknowledge Boundaries:** Understand that all UI interaction logic strictly resides in `app/bot/`, and pure business logic strictly resides in `app/core/`.
4. **Draft the Plan:** Conclude your intake step by explicitly outputting your proposed implementation plan, detailing exactly which layers and schemas will be modified. Wait for authorization before modifying the codebase.

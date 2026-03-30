# 📖 The Field Manual: Mr. Assistant Scripts

Welcome to your command center. Every script in this project exists to make your life easier and your code stronger. This guide explains which folder holds which tools.

---

## 🛠 `scripts/core/` (Architecture & Laws)
These are the most important scripts. They ensure the "Mister Starter Pack" standards are never violated.

| Script | Purpose | How to use |
| :--- | :--- | :--- |
| `architecture_inspector.py` | Automatically checks the 4-zone directory structure. | `python scripts/core/architecture_inspector.py` |
| `dev_constitution.py` | The "Robot Police." It reads your code and flags "Junior" mistakes. | `python scripts/core/dev_constitution.py` |
| `project_map.py` | Generates a clean overview of every file in the project. | `python scripts/core/project_map.py` |
| `tree_generator.py` | Rebuilds the `tree_structure.txt` file for documentation. | `python scripts/core/tree_generator.py` |

---

## 🔧 `scripts/maintenance/` (Dev Ops)
Helper tools for keeping your repository sync'd and healthy.

| Script | Purpose | How to use |
| :--- | :--- | :--- |
| `git_sync.py` | Performs a clean commit and push of your current work. | `python scripts/maintenance/git_sync.py` |

---

## 🧪 `scripts/tests/` (QA & Safety)
Scripts designed to test the system's resilience.

| Script | Purpose | How to use |
| :--- | :--- | :--- |
| `test_constitution.py` | Performs a "Fire Drill" to verify the enforcer catches errors. | `python scripts/tests/test_constitution.py` |
| `/constitution_tests/` | (Folder) Contains the exact "crime-filled" code used during fire drills. | No direct use. |

---

## 🏹 `scripts/tools/` (User Utilities)
Standalone tools for the user to interact with the bot's data.

| Script | Purpose | How to use |
| :--- | :--- | :--- |
| `view_ideas.py` | **[NEW]** The "Vault Auditor." Instantly lists all saved #ideas. | `python scripts/tools/view_ideas.py` |

---

> [!TIP]
> **Pro Tip**: Use these scripts often! For example, run the `architecture_inspector.py` before you ever run the bot to ensure your folders are perfectly self-healed.

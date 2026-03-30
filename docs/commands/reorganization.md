# 📂 Command Vault: Project Reorganization

This document explains the heavy-lifting commands used to classify and organize the `scripts/` directory into a professional, scalable structure.

---

## 🏗️ 1. Classified Directory Creation
To organize our tools, we moved from a flat list to a 4-zone classification:

```powershell
New-Item -Path scripts/core, scripts/maintenance, scripts/tests, scripts/tools -ItemType Directory -Force
```

### 🔍 What it does:
*   **`New-Item`**: The standard PowerShell way to create things.
*   **`-ItemType Directory`**: Explicitly tells Windows these are *Folders*, not files.
*   **`-Force`**: Ensures that if the folder already exists, it doesn't crash (it just ensures it's there).

---

## 🚚 2. The Great Migration (Moving Scripts)
Once the folders were ready, we migrated the scripts into their new homes:

```powershell
Move-Item -Path scripts/architecture_inspector.py, scripts/dev_constitution.py, scripts/project_map.py, scripts/tree_generator.py, scripts/tree_structure.txt -Destination scripts/core/
Move-Item -Path scripts/git_sync.py -Destination scripts/maintenance/
Move-Item -Path scripts/test_constitution.py, scripts/constitution_tests, scripts/temp_bad_code -Destination scripts/tests/
```

### 🔍 What it does:
*   **`Move-Item`**: Relocates files from the source to the destination.
*   **Classification Logic**: 
    *   **`core/`**: Architectural "must-haves."
    *   **`maintenance/`**: Daily dev-ops utilities.
    *   **`tests/`**: QA and "Fire Drill" tools.
    *   **`tools/`**: Standalone user utilities (like the Idea Viewer).

---

> [!TIP]
> **Pro Tip**: Use the `-Path` argument with a comma-separated list of files to move multiple items in a single line. This is much faster than running the command 10 times!

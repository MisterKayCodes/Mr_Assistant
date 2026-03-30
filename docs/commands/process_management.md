# 👻 Command Vault: Ghost Killing & Process Management

This document records the exact commands used to stabilize the Telegram bot by clearing "Ghost" processes and ensuring a clean, persistent deployment.

---

## 🪓 1. The Forceful Taskkill
When multiple terminals are open or the bot hangs, Windows doesn't always release the port. This command is the "Reset Button."

```powershell
taskkill /F /IM python.exe /T
```

### 🔍 What it does:
*   **`/F`**: Force. This tells Windows "I'm not asking, I'm telling." It immediately kills the process without waiting for it to say goodbye.
*   **`/IM python.exe`**: Image Name. It targets every process named `python.exe`. Since we are running the bot in Python, this catches every "Ghost" bot.
*   **`/T`**: Tree. This kills the "Tree" (all child processes), which often leads to the terminal window itself closing.

---

## 🚀 2. The Heartbeat Startup (run.bat)
Once the ghosts are cleared, we use a single entry point to fire up the entire architecture correctly:

```powershell
.\run.bat
```

### 🔍 What it does (The "Mister" Chain):
1.  **Architecture Check**: Calls `scripts/core/architecture_inspector.py` to ensure all folders exist.
2.  **Surgical Ghost Clean**: Calls `run.py` which searches for only `Mr_Assistant` processes specifically.
3.  **Manual Hot-Reload Loop**: Starts the bot in a manual loop so that any code change restarts the bot instantly.
4.  **Unbuffered Output**: Forces the terminal to show every single log line the millisecond it happens.

---

> [!CAUTION]
> **Warning**: Only run `taskkill /F /IM python.exe /T` if you want to stop ALL Python apps on your machine. If you are working on two different bots at once, this command will kill both!

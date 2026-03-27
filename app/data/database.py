from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import event
from config import config

# THE MISTER ASSISTANT WAY: 
# We use aiosqlite because we don't want the bot to "freeze" during a save.
DATABASE_URL = config.database_url

# 1. Create the Async Engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True, # Set to False in production, but True now so we can see the SQL!
)

# 2. Create the Session Maker (The factory that gives us database connections)
async_session_maker = async_sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

# --- THE SENIOR FIX: Enabling WAL Mode ---
# We run this as soon as a connection is made to ensure no locking.
@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

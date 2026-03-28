import asyncio
from app.data.database import engine
from app.data.models import Base, MessageType
from app.data.repository import save_message, get_recent_messages

async def test_memory():
    print("🚀 Starting Memory Sync Test...")
    
    # 1. Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[✓] Database Tables Checked/Created.")

    # 2. Simulate saving a message
    test_user_id = 123456789012345 # Large BigInteger ID
    success = await save_message(
        user_id=test_user_id,
        raw_text="Hello from the Test Script!",
        msg_type=MessageType.TEXT
    )
    
    if success:
        print("[✓] Message saved successfully!")
    else:
        print("[✗] Failed to save message.")
        return

    # 3. Verify retrieval
    history = await get_recent_messages(test_user_id)
    if history and len(history) > 0:
        print(f"[✓] Retrieved {len(history)} message(s).")
        print(f"    Latest: {history[0]['raw_text']} (Type: {history[0]['type']})")
    else:
        print("[✗] History fetch failed or empty.")

    print("\n🏁 Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_memory())

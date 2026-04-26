import aiosqlite
from datetime import datetime, timezone
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS warns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mod_id INTEGER NOT NULL,
                reason TEXT NOT NULL,
                expires_at TEXT NOT NULL
            )
        """)
        await db.commit()

async def add_warn(user_id: int, mod_id: int, reason: str, expires_at: datetime) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO warns (user_id, mod_id, reason, expires_at) VALUES (?, ?, ?, ?)",
            (user_id, mod_id, reason, expires_at.isoformat())
        )
        await db.commit()
        return cur.lastrowid

async def remove_warn(warn_id: int, user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "DELETE FROM warns WHERE id = ? AND user_id = ?", (warn_id, user_id)
        )
        await db.commit()
        return cur.rowcount > 0

async def get_warns(user_id: int) -> list[dict]:
    now = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM warns WHERE user_id = ? AND expires_at <= ?", (user_id, now))
        await db.commit()
        async with db.execute(
            "SELECT id, mod_id, reason, expires_at FROM warns WHERE user_id = ? ORDER BY id",
            (user_id,)
        ) as cur:
            rows = await cur.fetchall()
    return [{"id": r[0], "mod_id": r[1], "reason": r[2], "expires_at": r[3]} for r in rows]

async def remove_all_warns(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("DELETE FROM warns WHERE user_id = ?", (user_id,))
        await db.commit()
        return cur.rowcount

import sqlite3
from datetime import datetime

DB_PATH = "data/memories.db"


def create_memory_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_text TEXT NOT NULL,
            category TEXT,
            event_type TEXT,
            event_time TEXT,
            notes TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_memory(raw_text: str, category: str, event_type: str, event_time: str = None, notes: str = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO memories (
            raw_text,
            category,
            event_type,
            event_time,
            notes,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            raw_text,
            category,
            event_type,
            event_time,
            notes,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()


def get_recent_memories(limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT raw_text, category, event_type, event_time, notes, created_at
        FROM memories
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows
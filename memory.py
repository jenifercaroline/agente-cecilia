import sqlite3
from datetime import datetime

DB_PATH = "data/memories.db"

def create_memory_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_memory(content: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO memories (content, created_at) VALUES (?, ?)",
        (content, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()

def get_recent_memories(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT content, created_at FROM memories ORDER BY id DESC LIMIT ?",
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows
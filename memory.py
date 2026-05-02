import os
import sqlite3
from datetime import datetime

DB_PATH = "data/memories.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_memory_table():
    conn = get_connection()
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


def save_memory(raw_text, category, event_type, event_time=None, notes=None):
    conn = get_connection()
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
            datetime.now().isoformat(timespec="seconds"),
        )
    )

    conn.commit()
    conn.close()


def get_recent_memories(limit=10):
    conn = get_connection()
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


def get_today_memories():
    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().date().isoformat()

    cursor.execute(
        """
        SELECT raw_text, category, event_type, event_time, notes, created_at
        FROM memories
        WHERE DATE(created_at) = ?
        ORDER BY id DESC
        """,
        (today,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def search_memories(query, limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT raw_text, category, event_type, event_time, notes, created_at
        FROM memories
        WHERE
            raw_text LIKE ?
            OR category LIKE ?
            OR event_type LIKE ?
            OR notes LIKE ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            f"%{query}%",
            f"%{query}%",
            f"%{query}%",
            f"%{query}%",
            limit,
        )
    )

    rows = cursor.fetchall()
    conn.close()
    return rows
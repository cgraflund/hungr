import sqlite3
import os

from src.models import User

DB_NAME = os.getenv("DB_NAME")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            likes TEXT,   -- Comma-separated tags (e.g., 'sushi, ramen, vegetarian')
            dislikes TEXT -- Comma-separated tags (e.g., 'spicy, beef')
        )
    """)
    conn.commit()
    conn.close()

def add_user(name, likes="", dislikes=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, likes, dislikes) VALUES (?, ?, ?)", (name, likes, dislikes))
    conn.commit()
    conn.close()

def bulk_add_users(users):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.executemany(
        "INSERT INTO users (name, likes, dislikes) VALUES (?, ?, ?)",
        [(u["name"], u["likes"], u["dislikes"]) for u in users]
    )

    conn.commit()
    conn.close()

def get_user(name) -> User | None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT likes, dislikes FROM users WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return User(name=name, likes=row[0], dislikes=row[1])
    return None

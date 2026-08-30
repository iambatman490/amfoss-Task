import sqlite3
import datetime

DB_NAME = "ledger.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionary-like objects
    return conn

def init_db():
    """Creates the users table if it does not exist yet."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance INTEGER DEFAULT 500,
                last_daily TEXT,
                last_rob TEXT
            )
        """)
        conn.commit()

def get_user(user_id: int, username: str = "Unknown Pirate"):
    """Fetches user details or creates a new entry with 500 starter Berries."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cur.fetchone()
        if not user:
            cur.execute(
                "INSERT INTO users (user_id, username, balance) VALUES (?, ?, 500)",
                (user_id, username)
            )
            conn.commit()
            cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cur.fetchone()
        return dict(user)

def update_balance(user_id: int, amount: int):
    """Adds or subtracts Berries from a user's wallet."""
    with get_db() as conn:
        conn.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()

def set_timestamp(user_id: int, column: str):
    """Updates last_daily or last_rob cooldown timestamp with current UTC time."""
    now = datetime.datetime.utcnow().isoformat()
    with get_db() as conn:
        conn.execute(f"UPDATE users SET {column} = ? WHERE user_id = ?", (now, user_id))
        conn.commit()

def get_top_pirates(limit=5):
    """Queries the richest users sorted in descending order."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, balance FROM users ORDER BY balance DESC LIMIT ?", (limit,))
        return cur.fetchall()
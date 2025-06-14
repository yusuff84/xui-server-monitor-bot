import sqlite3
from config import ADMIN_IDS


def init_db():
    with sqlite3.connect("servers.db") as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                url TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS state (
                chat_id INTEGER PRIMARY KEY,
                waiting_for_input INTEGER DEFAULT 0
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY
            )
        """)
        c.execute("INSERT OR IGNORE INTO admins (id) VALUES (?)", (ADMIN_IDS[0],))


def is_admin(chat_id):
    with sqlite3.connect("servers.db") as conn:
        cur = conn.execute("SELECT 1 FROM admins WHERE id = ?", (chat_id,))
        return cur.fetchone() is not None


def add_admin(chat_id):
    with sqlite3.connect("servers.db") as conn:
        conn.execute("INSERT OR IGNORE INTO admins (id) VALUES (?)", (chat_id,))


def set_waiting(chat_id, waiting):
    with sqlite3.connect("servers.db") as conn:
        conn.execute("INSERT OR REPLACE INTO state (chat_id, waiting_for_input) VALUES (?, ?)", (chat_id, waiting))


def is_waiting(chat_id):
    with sqlite3.connect("servers.db") as conn:
        cur = conn.execute("SELECT waiting_for_input FROM state WHERE chat_id = ?", (chat_id,))
        row = cur.fetchone()
        return row and row[0] == 1


def save_server(chat_id, url):
    with sqlite3.connect("servers.db") as conn:
        conn.execute("INSERT INTO servers (chat_id, url) VALUES (?, ?)", (chat_id, url.rstrip("/")))


def get_servers(chat_id):
    with sqlite3.connect("servers.db") as conn:
        cur = conn.execute("SELECT id, url FROM servers WHERE chat_id = ?", (chat_id,))
        return cur.fetchall()


def delete_server(chat_id, server_id):
    with sqlite3.connect("servers.db") as conn:
        conn.execute("DELETE FROM servers WHERE id = ? AND chat_id = ?", (server_id, chat_id))

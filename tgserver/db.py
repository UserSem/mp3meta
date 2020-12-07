import sqlite3

from telegram.user import User

import config


conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)


def init_db():
    cursor = conn.cursor()
    cursor.executescript(
        "CREATE TABLE IF NOT EXISTS users ("
        "  id TEXT PRIMARY KEY,"
        "  name TEXT NOT NULL,"
        "  is_staff BOOLEAN DEFAULT false"        
        ");"
        "CREATE TABLE IF NOT EXISTS membership ("
        "  group_name TEXT NOT NULL,"
        "  user_id TEXT NOT NULL,"
        "  is_admin BOOLEAN default false"
        ");"
        "CREATE TABLE IF NOT EXISTS files ("
        "  group_name TEXT NOT NULL,"
        "  file_name TEXT NOT NULL"
        ");"
        "CREATE TABLE IF NOT EXISTS tags ("
        "  file_name TEXT NOT NULL,"
        "  tag_name TEXT NOT NULL,"
        "  tag_value TEXT"
        ");"
        "CREATE TABLE IF NOT EXISTS requests ("
        "  group_name TEXT NOT NULL,"
        "  user_id TEXT NOT NULL"
        ");"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (config.ADMIN_ID, ))
    data = cursor.fetchone()
    if data is None:
        conn.cursor().execute("INSERT INTO users VALUES (?, ?, ?)",
                              (config.ADMIN_ID, "Superadmin", True))
        conn.commit()


def add_user(user: User):
    cursor = conn.execute("SELECT * FROM users where id=?", (user.id, ))
    data = cursor.fetchone()
    if data is not None:
        return None
    name = [txt for txt in (user.first_name, user.username, user.last_name) if txt is not None]
    if not name:
        return "Bad name"
    conn.execute("INSERT INTO users VALUES (?, ?, ?)", (user.id, ' '.join(name), False))
    conn.commit()


def add_request(group: str, user_id: str):
    conn.execute("INSERT INTO requests VALUES (?, ?)", (group, user_id))
    conn.commit()
    data = conn.execute("SELECT user_id FROM membership WHERE is_admin=true and group_name=?", (group, )).fetchall()
    if not data:
        data = conn.execute("SELECT id FROM users WHERE is_staff=true").fetchall()
    return [d[0] for d in data]


init_db()

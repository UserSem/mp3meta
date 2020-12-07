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


def user_is_admin(user_id: str, group_name: str='') -> bool:
    # Checking for superadmin
    data = conn.execute("SELECT is_staff FROM users WHERE id = ?", (user_id, )).fetchall()
    if data and data[0][0]:
        return True
    if not group_name:
        return False

    # Checking for group admin
    data = conn.execute("SELECT is_admin FROM membership WHERE group_name = ? AND user_id = ?",
                        (group_name, user_id)).fetchall()
    if data and data[0][0]:
        return True
    return False


def user_in_group(user_id: str, group_name: str) -> bool:
    data = conn.execute("SELECT user_id FROM membership WHERE user_id = ? AND group_name = ?",
                        (user_id, group_name)).fetchall()
    return bool(data)


def request_exists(user_id: str, group_name: str) -> bool:
    data = conn.execute("SELECT user_id FROM requests WHERE user_id = ? AND group_name = ?",
                        (user_id, group_name)).fetchall()
    return bool(data)


def add_user_to_group(user_id: str, group_name: str, sender_id: str):
    if not user_is_admin(sender_id, group_name):
        return 'No rights'
    if user_in_group(user_id, group_name):
        return "Already in group"
    if not request_exists(user_id, group_name):
        return "No request"
    conn.execute("DELETE FROM requests WHERE user_id = ? AND group_name = ?",
                 (user_id, group_name))
    conn.execute("INSERT INTO membership VALUES (?, ?, ?)",
                 (group_name, user_id, False))
    conn.commit()




init_db()

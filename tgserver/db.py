import sqlite3

from telegram.user import User

import config


conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)


def init_db():
    cursor = conn.cursor()
    cursor.executescript(
        "CREATE TABLE IF NOT EXISTS users ("
        "  user_id TEXT PRIMARY KEY,"
        "  name TEXT NOT NULL,"
        "  is_staff BOOLEAN DEFAULT false,"
        "  current_file_name TEXT"        
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
    cursor.execute("SELECT * FROM users WHERE user_id=?", (config.ADMIN_ID, ))
    data = cursor.fetchone()
    if data is None:
        conn.cursor().execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                              (config.ADMIN_ID, "Superadmin", True, None))
        conn.commit()


def add_user(user: User):
    cursor = conn.execute("SELECT * FROM users where user_id=?", (user.id, ))
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
        data = conn.execute("SELECT user_id FROM users WHERE is_staff=true").fetchall()
    return [d[0] for d in data]


def user_is_admin(user_id: str, group_name: str='') -> bool:
    # Checking for superadmin
    data = conn.execute("SELECT is_staff FROM users WHERE user_id = ?", (user_id, )).fetchall()
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


def get_user_groups(user_id: str) -> list:
    data = conn.execute("SELECT group_name FROM membership WHERE user_id = ?",
                        (user_id, )).fetchall()
    return [d[0] for d in data]


def add_file_to_db(file_name: str, group_name: str):
    conn.execute("INSERT INTO files VALUES (?, ?)",
                 (group_name, file_name))
    conn.commit()


def set_current_file(user_id: str, file_name: str):
    conn.execute("UPDATE users SET current_file_name = ? WHERE user_id = ?",
                 (file_name, user_id))
    conn.commit()


def write_tags_to_db(file_name: str, tags: dict):
    conn.execute("DELETE FROM tags WHERE file_name = ?",
                 (file_name, ))
    for key, val in tags.items():
        if val:
            conn.execute("INSERT INTO tags VALUES (?, ?, ?)",
                         (file_name, key, val))
    conn.commit()


def search_files(terms: list, group_name: str) -> list:
    result = set()
    data = conn.execute("SELECT file_name FROM files WHERE group_name = ?",
                         (group_name, )).fetchall()
    files = [d[0] for d in data]
    for term in terms:
        for file in files:
            if term.lower() in file.lower():
                result.add(file)
            else:
                data = conn.execute("SELECT file_name FROM tags WHERE file_name = ? AND tag_value LIKE ?",
                         (file, '%'+term+'%')).fetchall()
                for file_name in data:
                    result.add(file_name[0])
    return sorted(list(result))


init_db()

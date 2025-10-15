import sqlite3 as sql


def get_all_users(exclude_username=None, search_query=None):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    if search_query:
        if exclude_username:
            cur.execute(
                (
                    "SELECT username FROM user_data "
                    "WHERE username != ? AND username LIKE ?"
                ),
                (exclude_username, f"%{search_query}%"),
            )
        else:
            cur.execute(
                "SELECT username FROM user_data WHERE username LIKE ?",
                (f"%{search_query}%",),
            )
    else:
        if exclude_username:
            cur.execute(
                "SELECT username FROM user_data WHERE username != ?",
                (exclude_username,),
            )
        else:
            cur.execute("SELECT username FROM user_data")
    users = [row[0] for row in cur.fetchall()]
    con.close()
    return users


def get_messages(user1, user2):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute(
        """
        SELECT sender, recipient, content, timestamp FROM messages
        WHERE (sender=? AND recipient=?) OR (sender=? AND recipient=?)
        ORDER BY timestamp ASC
        """,
        (user1, user2, user2, user1),
    )
    messages = cur.fetchall()
    con.close()
    return messages


def add_message(sender, recipient, content, timestamp):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute(
        (
            "INSERT INTO messages (sender, recipient, content, timestamp) "
            "VALUES (?, ?, ?, ?)"
        ),
        (sender, recipient, content, timestamp),
    )
    con.commit()
    con.close()


def listExtension():
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM extension").fetchall()
    con.close()
    return data


def add_user(username, password, email, account_creation_date, avatar=None):
    if not avatar:
        avatar = "static/images/avatar.jpg"
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO user_data (username, password, email, account_creation_date, avatar) VALUES (?, ?, ?, ?, ?)",
            (username, password, email, account_creation_date, avatar),
        )
        con.commit()
        return True
    except sql.IntegrityError:
        return False
    finally:
        con.close()


def get_user(username):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM user_data WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    return user


def update_bio(username, bio):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute(
        "UPDATE user_data SET bio = ? WHERE username = ?",
        (bio, username),
    )
    con.commit()
    con.close()


def update_avatar(username, avatar_path):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute(
        "UPDATE user_data SET avatar = ? WHERE username = ?", (avatar_path, username)
    )
    con.commit()
    con.close()


def get_avatar(username):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute("SELECT avatar FROM user_data WHERE username = ?", (username,))
    row = cur.fetchone()
    con.close()
    if row and row[0]:
        return row[0]
    return "static/images/avatar.jpg"


def get_recent_chats(username):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute(
        """
        SELECT
            CASE
                WHEN sender = ? THEN recipient
                ELSE sender
            END AS chat_partner,
            MAX(timestamp) as last_time
        FROM messages
        WHERE sender = ? OR recipient = ?
        GROUP BY chat_partner
        ORDER BY last_time DESC
    """,
        (username, username, username),
    )
    chats = cur.fetchall()
    con.close()
    return [row[0] for row in chats]

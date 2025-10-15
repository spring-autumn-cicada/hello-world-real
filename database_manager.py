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


def add_user(username, password, email, account_creation_date):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO user_data "
            "(username, password, email, account_creation_date) "
            "VALUES (?, ?, ?, ?)",
            (
                username,
                password,
                email,
                account_creation_date,
            ),
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

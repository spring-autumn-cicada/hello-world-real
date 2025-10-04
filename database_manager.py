import sqlite3 as sql


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

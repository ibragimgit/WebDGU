import sqlite3

with sqlite3.connect('login_password.db') as db_lp:
    cursor_db = db_lp.cursor()
    sql_create = '''CREATE TABLE IF NOT EXISTS passwords (
        login TEXT PRIMARY KEY,
        password TEXT NOT NULL
    );'''

    cursor_db.execute(sql_create)
    db_lp.commit()

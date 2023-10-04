import sqlite3

with sqlite3.connect('login_password.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            full_name TEXT,
            passport_number TEXT,
            course INTEGER,
            groups TEXT,
            project_name TEXT,
            project_content TEXT
        )
    ''')
    conn.commit()
import sqlite3

def create_database():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()

    # Створення таблиці users
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname VARCHAR(100),
            email VARCHAR(100) UNIQUE
        )
    ''')

    # Створення таблиці status
    cur.execute('''
        CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) UNIQUE
        )
    ''')

    # Створення таблиці tasks
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(100),
            description TEXT,
            status_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (status_id) REFERENCES status (id),
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

create_database()

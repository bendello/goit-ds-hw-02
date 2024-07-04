from faker import Faker
import sqlite3

def seed_database():
    fake = Faker()
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()

    # Очищення таблиць перед вставкою нових даних
    cur.execute('DELETE FROM tasks')
    cur.execute('DELETE FROM users')
    cur.execute('DELETE FROM status')

    # Вставка статусів
    statuses = [('new',), ('in progress',), ('completed',)]
    cur.executemany('INSERT INTO status (name) VALUES (?)', statuses)

    # Вставка користувачів
    users = []
    for _ in range(10):
        users.append((fake.name(), fake.email()))

    cur.executemany('INSERT INTO users (fullname, email) VALUES (?, ?)', users)

    # Вставка завдань
    tasks = []
    for _ in range(30):
        tasks.append((fake.sentence(nb_words=4), fake.text(), fake.random_int(min=1, max=3), fake.random_int(min=1, max=10)))

    cur.executemany('INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)', tasks)

    conn.commit()
    conn.close()

seed_database()


import sqlite3

def execute_queries():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()

    # 1. Отримати всі завдання певного користувача
    user_id = 1
    cur.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
    print(f"Tasks for user_id {user_id}:", cur.fetchall())

    # 2. Вибрати завдання за певним статусом
    status_name = 'new'
    cur.execute('SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = ?)', (status_name,))
    print(f"Tasks with status {status_name}:", cur.fetchall())

    # 3. Оновити статус конкретного завдання
    task_id = 1
    new_status_name = 'in progress'
    cur.execute('UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = ?) WHERE id = ?', (new_status_name, task_id))
    conn.commit()

    # 4. Отримати список користувачів, які не мають жодного завдання
    cur.execute('SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)')
    print("Users without tasks:", cur.fetchall())

    # 5. Додати нове завдання для конкретного користувача
    new_task = ('New Task', 'Description of the new task', 1, user_id)
    cur.execute('INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)', new_task)
    conn.commit()

    # 6. Отримати всі завдання, які ще не завершено
    cur.execute('SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = "completed")')
    print("Uncompleted tasks:", cur.fetchall())

    # 7. Видалити конкретне завдання
    delete_task_id = 2
    cur.execute('DELETE FROM tasks WHERE id = ?', (delete_task_id,))
    conn.commit()

    # 8. Знайти користувачів з певною електронною поштою
    email_domain = '%@example.com'
    cur.execute('SELECT * FROM users WHERE email LIKE ?', (email_domain,))
    print(f"Users with email domain {email_domain}:", cur.fetchall())

    # 9. Оновити ім'я користувача
    new_fullname = 'Updated Name'
    cur.execute('UPDATE users SET fullname = ? WHERE id = ?', (new_fullname, user_id))
    conn.commit()

    # 10. Отримати кількість завдань для кожного статусу
    cur.execute('SELECT status.name, COUNT(tasks.id) FROM tasks JOIN status ON tasks.status_id = status.id GROUP BY status.name')
    print("Task counts by status:", cur.fetchall())

    # 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
    cur.execute('SELECT tasks.* FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.email LIKE ?', (email_domain,))
    print(f"Tasks assigned to users with email domain {email_domain}:", cur.fetchall())

    # 12. Отримати список завдань, що не мають опису
    cur.execute('SELECT * FROM tasks WHERE description IS NULL OR description = ""')
    print("Tasks without description:", cur.fetchall())

    # 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
    cur.execute('''
        SELECT users.fullname, tasks.title FROM users 
        JOIN tasks ON users.id = tasks.user_id 
        JOIN status ON tasks.status_id = status.id 
        WHERE status.name = 'in progress'
    ''')
    print("Users and their tasks with status 'in progress':", cur.fetchall())

    # 14. Отримати користувачів та кількість їхніх завдань
    cur.execute('''
        SELECT users.fullname, COUNT(tasks.id) FROM users 
        LEFT JOIN tasks ON users.id = tasks.user_id 
        GROUP BY users.fullname
    ''')
    print("Users and their task counts:", cur.fetchall())

    conn.close()

execute_queries()

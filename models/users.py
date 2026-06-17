from db import fetch_one, fetch_all, execute_query

def get_user_by_login(username, password):
    return fetch_one(
        'SELECT * FROM users WHERE username=%s AND password=%s',
        (username, password),
    )


def get_all_users():
    return fetch_all('SELECT id, username, role, created_at FROM users ORDER BY id DESC')

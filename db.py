import mysql.connector
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(query, params=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)

    cursor.execute(query, params or ())
    result = cursor.fetchall()

    cursor.close()
    connection.close()
    return result


def fetch_one(query, params=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)

    cursor.execute(query, params or ())
    result = cursor.fetchone()

    cursor.close()
    connection.close()
    return result


def execute_query(query, params=None):
    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(query, params or ())
    connection.commit()

    cursor.close()
    connection.close()
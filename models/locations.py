from db import fetch_all, fetch_one, execute_query


def get_locations():
    return fetch_all(
        '''
        SELECT *
        FROM locations
        WHERE is_active = 1
        ORDER BY id
        '''
    )


def get_location(location_id):
    return fetch_one(
        '''
        SELECT *
        FROM locations
        WHERE id = %s
        ''',
        (location_id,)
    )


def create_location(name, address):
    execute_query(
        '''
        INSERT INTO locations (name, address)
        VALUES (%s, %s)
        ''',
        (name, address)
    )
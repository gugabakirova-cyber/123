from db import fetch_all, execute_query


def get_expenses(location_id=None):

    query = '''
        SELECT *
        FROM expenses
        WHERE 1=1
    '''

    params = []

    if location_id:
        query += ' AND location_id = %s'
        params.append(location_id)

    query += ' ORDER BY created_at DESC'

    return fetch_all(
        query,
        tuple(params)
    )


def create_expense(
    title,
    category,
    amount,
    comment='',
    location_id=None
):

    return execute_query(
        '''
        INSERT INTO expenses (
            title,
            category,
            amount,
            comment,
            location_id
        )
        VALUES (%s,%s,%s,%s,%s)
        ''',
        (
            title,
            category,
            amount,
            comment,
            location_id
        )
    )
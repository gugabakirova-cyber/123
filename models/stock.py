from db import fetch_all, execute_query


def add_stock(product_id, quantity, comment='', location_id=None):
    execute_query(
        '''
        INSERT INTO stock_balances (product_id, location_id, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
        ''',
        (product_id, location_id, quantity)
    )

    execute_query(
        '''
        INSERT INTO stock_movements (
            product_id,
            location_id,
            movement_type,
            quantity,
            comment
        )
        VALUES (%s, %s, %s, %s, %s)
        ''',
        (
            product_id,
            location_id,
            'income',
            quantity,
            comment
        )
    )


def write_off_stock(product_id, quantity, comment='', location_id=None):
    execute_query(
        '''
        INSERT INTO stock_balances (product_id, location_id, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity = quantity - VALUES(quantity)
        ''',
        (product_id, location_id, quantity)
    )

    execute_query(
        '''
        INSERT INTO stock_movements (
            product_id,
            location_id,
            movement_type,
            quantity,
            comment
        )
        VALUES (%s, %s, %s, %s, %s)
        ''',
        (
            product_id,
            location_id,
            'write_off',
            quantity,
            comment
        )
    )


def get_stock_history(search='', date_from='', date_to='', location_id=None):
    query = '''
        SELECT
            sm.*,
            p.name AS product_name
        FROM stock_movements sm
        JOIN products p ON p.id = sm.product_id
        WHERE 1=1
    '''

    params = []

    if location_id:
        query += ' AND sm.location_id = %s'
        params.append(location_id)

    if search:
        query += ' AND p.name LIKE %s'
        params.append(f'%{search}%')

    if date_from:
        query += ' AND DATE(sm.created_at) >= %s'
        params.append(date_from)

    if date_to:
        query += ' AND DATE(sm.created_at) <= %s'
        params.append(date_to)

    query += ' ORDER BY sm.created_at DESC'

    return fetch_all(query, tuple(params))


def get_stock_balances(location_id):
    return fetch_all(
        '''
        SELECT
            p.id,
            p.name,
            p.category,
            p.unit,
            p.purchase_price,
            p.sale_price,
            p.min_quantity,
            COALESCE(sb.quantity, 0) AS quantity
        FROM products p
        LEFT JOIN stock_balances sb
            ON sb.product_id = p.id
            AND sb.location_id = %s
        WHERE p.location_id = %s
        ORDER BY p.name
        ''',
        (location_id, location_id)
    )

def set_stock_balance(product_id, quantity, location_id):
    execute_query(
        '''
        INSERT INTO stock_balances (product_id, location_id, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity = VALUES(quantity)
        ''',
        (product_id, location_id, quantity)
    )
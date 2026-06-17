from db import fetch_all, fetch_one, execute_query


def get_products(search='', location_id=None):
    query = '''
        SELECT *
        FROM products
        WHERE 1=1
    '''

    params = []

    if location_id:
        query += ' AND location_id = %s'
        params.append(location_id)

    if search:
        query += ' AND (name LIKE %s OR category LIKE %s)'
        like = f'%{search}%'
        params.extend([like, like])

    query += ' ORDER BY name'

    return fetch_all(query, tuple(params))


def get_product(product_id, location_id=None):
    query = '''
        SELECT *
        FROM products
        WHERE id = %s
    '''

    params = [product_id]

    if location_id:
        query += ' AND location_id = %s'
        params.append(location_id)

    return fetch_one(query, tuple(params))


def create_product(
    name,
    category,
    unit,
    purchase_price,
    sale_price,
    quantity,
    min_quantity,
    location_id=None
):
    return execute_query(
        '''
        INSERT INTO products (
            name,
            category,
            unit,
            purchase_price,
            sale_price,
            quantity,
            min_quantity,
            location_id
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ''',
        (
            name,
            category,
            unit,
            purchase_price,
            sale_price,
            quantity,
            min_quantity,
            location_id
        )
    )


def update_product(
    product_id,
    name,
    category,
    unit,
    purchase_price,
    sale_price,
    quantity,
    min_quantity,
    location_id=None
):
    query = '''
        UPDATE products
        SET
            name = %s,
            category = %s,
            unit = %s,
            purchase_price = %s,
            sale_price = %s,
            quantity = %s,
            min_quantity = %s
        WHERE id = %s
    '''

    params = [
        name,
        category,
        unit,
        purchase_price,
        sale_price,
        quantity,
        min_quantity,
        product_id
    ]

    if location_id:
        query += ' AND location_id = %s'
        params.append(location_id)

    execute_query(query, tuple(params))


def delete_product(product_id, location_id=None):
    query = '''
        DELETE FROM products
        WHERE id = %s
    '''

    params = [product_id]

    if location_id:
        query += ' AND location_id = %s'
        params.append(location_id)

    execute_query(query, tuple(params))


def low_stock_products(location_id=None):
    query = '''
        SELECT *
        FROM products
        WHERE quantity <= min_quantity
    '''

    params = []

    if location_id:
        query += ' AND location_id = %s'
        params.append(location_id)

    query += ' ORDER BY quantity ASC'

    return fetch_all(query, tuple(params))
from db import fetch_all, execute_query
from models.stock import write_off_stock


def get_sales(location_id=None):
    query = '''
        SELECT
            s.*,
            p.name AS product_name,
            l.name AS location_name
        FROM sales s
        JOIN products p ON p.id = s.product_id
        LEFT JOIN locations l ON l.id = s.location_id
        WHERE 1=1
    '''

    params = []

    if location_id:
        query += ' AND s.location_id = %s'
        params.append(location_id)

    query += ' ORDER BY s.created_at DESC'

    return fetch_all(query, tuple(params))

def create_sale(product_id, quantity, price, location_id=None, writeoff_stock=True, comment='Продажа товара'):
    total = float(quantity) * float(price)

    sale_id = execute_query(
        '''
        INSERT INTO sales (
            product_id,
            location_id,
            quantity,
            price,
            total
        )
        VALUES (%s, %s, %s, %s, %s)
        ''',
        (
            product_id,
            location_id,
            quantity,
            price,
            total
        )
    )

    if writeoff_stock:
        write_off_stock(
            product_id,
            quantity,
            comment,
            location_id
        )

    return sale_id

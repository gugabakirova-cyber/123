from db import fetch_all, fetch_one


def dashboard_stats(location_id=None):
    params = []

    products_query = '''
        SELECT COUNT(*) AS total
        FROM products
        WHERE 1=1
    '''

    sales_query = '''
        SELECT COUNT(*) AS total
        FROM sales
        WHERE 1=1
    '''

    expenses_query = '''
        SELECT COUNT(*) AS total
        FROM expenses
        WHERE 1=1
    '''

    low_stock_query = '''
        SELECT COUNT(*) AS total
        FROM products
        WHERE quantity <= min_quantity
    '''

    if location_id:
        products_query += ' AND location_id = %s'
        sales_query += ' AND location_id = %s'
        expenses_query += ' AND location_id = %s'
        low_stock_query += ' AND location_id = %s'
        params = [location_id]

    products = fetch_one(products_query, tuple(params))
    sales = fetch_one(sales_query, tuple(params))
    expenses = fetch_one(expenses_query, tuple(params))
    low_stock = fetch_one(low_stock_query, tuple(params))

    return {
        'products_count': products['total'],
        'sales_count': sales['total'],
        'expenses_count': expenses['total'],
        'low_stock_count': low_stock['total'],
    }


def top_products(location_id=None):
    query = '''
        SELECT
            p.name,
            SUM(s.quantity) AS quantity,
            SUM(s.total) AS total
        FROM sales s
        JOIN products p ON p.id = s.product_id
        WHERE 1=1
    '''

    params = []

    if location_id:
        query += ' AND s.location_id = %s'
        params.append(location_id)

    query += '''
        GROUP BY p.id, p.name
        ORDER BY total DESC
        LIMIT 5
    '''

    return fetch_all(query, tuple(params))


def sales_by_products(location_id=None):
    query = '''
        SELECT
            p.name,
            SUM(s.total) AS total
        FROM sales s
        JOIN products p ON p.id = s.product_id
        WHERE 1=1
    '''

    params = []

    if location_id:
        query += ' AND s.location_id = %s'
        params.append(location_id)

    query += '''
        GROUP BY p.id, p.name
        ORDER BY total DESC
    '''

    return fetch_all(query, tuple(params))


def expenses_by_categories(location_id=None):
    query = '''
        SELECT
            category,
            SUM(amount) AS total
        FROM expenses
        WHERE 1=1
    '''

    params = []

    if location_id:
        query += ' AND location_id = %s'
        params.append(location_id)

    query += '''
        GROUP BY category
        ORDER BY total DESC
    '''

    return fetch_all(query, tuple(params))
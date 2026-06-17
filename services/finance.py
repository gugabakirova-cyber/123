from db import fetch_one, fetch_all


def money(value):
    return round(float(value or 0), 2)


def get_finance_summary(location_id=None):

    sales_query = '''
        SELECT
        COALESCE(SUM(total),0) AS total
        FROM sales
        WHERE 1=1
    '''

    expenses_query = '''
        SELECT
        COALESCE(SUM(amount),0) AS total
        FROM expenses
        WHERE 1=1
    '''

    stock_query = '''
        SELECT
        COALESCE(
            SUM(
                sb.quantity * p.purchase_price
            ),
            0
        ) AS total
        FROM stock_balances sb
        JOIN products p
        ON p.id = sb.product_id
        WHERE 1=1
    '''

    params = []

    if location_id:
        sales_query += ' AND location_id=%s'
        expenses_query += ' AND location_id=%s'
        stock_query += ' AND sb.location_id=%s'
        params = [location_id]

    sales = fetch_one(
        sales_query,
        tuple(params)
    )

    expenses = fetch_one(
        expenses_query,
        tuple(params)
    )

    stock = fetch_one(
        stock_query,
        tuple(params)
    )

    income = money(
        sales['total']
    )

    expense = money(
        expenses['total']
    )

    return {
        'income': income,
        'expenses': expense,
        'profit': money(
            income - expense
        ),
        'stock_value': money(
            stock['total']
        )
    }


def get_monthly_finance(location_id=None):

    sales_query = '''
        SELECT
        DATE_FORMAT(created_at,'%Y-%m')
        AS period,

        SUM(total)
        AS income,

        0 AS expenses

        FROM sales
        WHERE 1=1
    '''

    expense_query = '''
        SELECT
        DATE_FORMAT(created_at,'%Y-%m')
        AS period,

        0 AS income,

        SUM(amount)
        AS expenses

        FROM expenses
        WHERE 1=1
    '''

    params=[]

    if location_id:
        sales_query += ' AND location_id=%s'
        expense_query += ' AND location_id=%s'
        params=[location_id]

    sales_query += ' GROUP BY period'
    expense_query += ' GROUP BY period'

    return fetch_all(
        f'''
        {sales_query}

        UNION ALL

        {expense_query}

        ORDER BY period
        ''',
        tuple(params + params)
    )
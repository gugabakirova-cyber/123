from db import fetch_all, fetch_one, execute_query


def create_inventory_check(location_id, username):
    execute_query(
        '''
        INSERT INTO inventory_checks(
            location_id,
            username
        )
        VALUES(%s,%s)
        ''',
        (
            location_id,
            username
        )
    )

    row = fetch_one(
        '''
        SELECT id
        FROM inventory_checks
        WHERE location_id = %s
        AND username = %s
        ORDER BY id DESC
        LIMIT 1
        ''',
        (
            location_id,
            username
        )
    )

    return row['id']


def add_inventory_item(
    check_id,
    product_id,
    system_quantity,
    actual_quantity
):

    difference = (
        float(actual_quantity)
        -
        float(system_quantity)
    )

    execute_query(
        '''
        INSERT INTO inventory_items(
            check_id,
            product_id,
            system_quantity,
            actual_quantity,
            difference_quantity
        )
        VALUES(%s,%s,%s,%s,%s)
        ''',
        (
            check_id,
            product_id,
            system_quantity,
            actual_quantity,
            difference
        )
    )


def get_inventory_history(location_id=None):

    query = '''
        SELECT
            ic.*,
            (
                SELECT COUNT(*)
                FROM inventory_items ii
                WHERE ii.check_id = ic.id
            ) AS items_count
        FROM inventory_checks ic
        WHERE 1=1
    '''

    params = []

    if location_id:
        query += '''
        AND ic.location_id = %s
        '''
        params.append(location_id)

    query += '''
    ORDER BY ic.created_at DESC
    '''

    return fetch_all(
        query,
        tuple(params)
    )

def get_inventory_items(check_id):
    return fetch_all(
        '''
        SELECT
            ii.*,
            p.name AS product_name,
            p.unit
        FROM inventory_items ii
        JOIN products p ON p.id = ii.product_id
        WHERE ii.check_id = %s
        ORDER BY p.name
        ''',
        (check_id,)
    )
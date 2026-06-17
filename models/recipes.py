from db import fetch_all, execute_query


def get_recipe(dish_name, location_id=None):
    query = '''
        SELECT
            r.product_id,
            r.amount,
            r.unit,
            r.output_quantity,
            r.output_unit,
            p.name AS product_name,
            p.unit AS product_unit,
            p.purchase_price
        FROM recipes r
        JOIN products p ON p.id = r.product_id
        WHERE LOWER(TRIM(r.dish_name)) = LOWER(TRIM(%s))
    '''

    params = [dish_name]

    if location_id:
        query += '''
            AND (r.location_id = %s OR r.location_id IS NULL)
        '''
        params.append(location_id)

    query += ' ORDER BY p.name'

    return fetch_all(query, tuple(params))


def get_all_recipes(location_id=None):
    query = '''
        SELECT
            r.id,
            r.dish_name,
            r.amount,
            r.unit,
            r.output_quantity,
            r.output_unit,
            p.name AS product_name,
            p.unit AS product_unit,
            p.purchase_price
        FROM recipes r
        JOIN products p ON p.id = r.product_id
        WHERE 1=1
    '''

    params = []

    if location_id:
        query += ' AND r.location_id = %s'
        params.append(location_id)

    query += ' ORDER BY r.dish_name, p.name'

    return fetch_all(query, tuple(params))


def get_recipes_grouped(location_id=None):
    rows = get_all_recipes(location_id)
    grouped = {}

    for row in rows:
        name = row['dish_name']
        if name not in grouped:
            grouped[name] = {
                'dish_name': name,
                'output_quantity': row.get('output_quantity') or 1,
                'output_unit': row.get('output_unit') or 'порция',
                'ingredients': [],
                'cost': 0
            }
        amount = float(row.get('amount') or 0)
        price = float(row.get('purchase_price') or 0)

        unit = str(row.get('unit') or '').lower()
        product_unit = str(row.get('product_unit') or '').lower()

        if product_unit in ['кг', 'kg'] and unit in ['г', 'гр', 'g']:
            cost = amount * price / 1000
        elif product_unit in ['г', 'гр', 'g'] and unit in ['кг', 'kg']:
            cost = amount * 1000 * price
        elif product_unit in ['л', 'l'] and unit in ['мл', 'ml']:
            cost = amount * price / 1000
        elif product_unit in ['мл', 'ml'] and unit in ['л', 'l']:
            cost = amount * 1000 * price
        else:
            cost = amount * price

        ingredient = dict(row)
        ingredient['cost'] = round(cost, 2)
        grouped[name]['ingredients'].append(ingredient)
        grouped[name]['cost'] += cost

    result = []
    for item in grouped.values():
        item['cost'] = round(item['cost'], 2)
        result.append(item)

    return result


def create_recipe(dish_name, product_id, amount, unit, location_id=None, output_quantity=1, output_unit='порция'):
    execute_query(
        '''
        INSERT INTO recipes (
            dish_name,
            product_id,
            amount,
            unit,
            location_id,
            output_quantity,
            output_unit
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''',
        (dish_name, product_id, amount, unit, location_id, output_quantity, output_unit)
    )
def delete_recipe(dish_name):
    execute_query(
        '''
        DELETE FROM recipes
        WHERE dish_name = %s
        ''',
        (dish_name,)
    )
def update_recipe_header(old_dish_name, dish_name, output_quantity, output_unit):
    execute_query(
        '''
        UPDATE recipes
        SET
            dish_name = %s,
            output_quantity = %s,
            output_unit = %s
        WHERE dish_name = %s
        ''',
        (dish_name, output_quantity, output_unit, old_dish_name)
    )
def update_recipe_full(old_dish_name, dish_name, output_quantity, output_unit, product_ids, amounts, units):
    execute_query(
        '''
        DELETE FROM recipes
        WHERE dish_name = %s
        ''',
        (old_dish_name,)
    )

    for product_id, amount, unit in zip(product_ids, amounts, units):
        if not product_id or not amount or not unit:
            continue

        execute_query(
            '''
            INSERT INTO recipes (
                dish_name,
                product_id,
                amount,
                unit,
                location_id,
                output_quantity,
                output_unit
            )
            VALUES (%s, %s, %s, %s, NULL, %s, %s)
            ''',
            (dish_name, product_id, amount, unit, output_quantity, output_unit)
        )
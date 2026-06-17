from models.recipes import get_recipe
from models.stock import write_off_stock
from services.unit_converter import convert_quantity, format_quantity


def write_off_by_report_items(items, location_id=None):
    results = []

    for item in items:
        dish_name = item['name']
        quantity = item['quantity']

        recipe = get_recipe(dish_name, location_id)

        if not recipe:
            results.append({
                'dish_name': dish_name,
                'quantity': quantity,
                'status': 'no_recipe',
                'message': 'Техкарта не найдена'
            })
            continue

        for ingredient in recipe:
            ingredient_amount = float(ingredient['amount']) * float(quantity)
            stock_amount = convert_quantity(
                ingredient_amount,
                ingredient['unit'],
                ingredient.get('product_unit')
            )

            write_off_stock(
                ingredient['product_id'],
                stock_amount,
                f"Автосписание по отчету iiko: {dish_name} x {quantity}; {ingredient['product_name']} {format_quantity(ingredient_amount)} {ingredient['unit']} ({format_quantity(stock_amount)} {ingredient.get('product_unit')})",
                location_id
            )

        results.append({
            'dish_name': dish_name,
            'quantity': quantity,
            'status': 'success',
            'message': 'Списано по техкарте'
        })

    return results

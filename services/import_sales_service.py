from models.products import get_products, create_product
from models.sales import create_sale


def _normalize(value):
    return str(value or '').lower().strip()


def _find_or_create_sale_product(item, location_id):
    """Находит или создает готовую позицию для записи в таблицу продаж."""
    products = get_products(location_id=location_id)
    name = item.get('name')

    for product in products:
        if _normalize(product.get('name')) == _normalize(name):
            return product['id']

    # Для импортированных продаж создаем служебный товар без складского остатка.
    # Ингредиенты списываются отдельно по техкарте, поэтому сам товар со склада не списываем.
    return create_product(
        name,
        'Готовая продукция',
        'шт',
        0,
        item.get('price') or 0,
        0,
        0,
        location_id
    )


def create_sales_from_iiko_items(items, location_id=None):
    results = []

    for item in items:
        quantity = float(item.get('quantity') or 0)
        total = float(item.get('total') or 0)
        price = float(item.get('price') or 0)

        if quantity <= 0:
            results.append({
                'name': item.get('name'),
                'quantity': quantity,
                'status': 'danger',
                'message': 'Количество не распознано'
            })
            continue

        if not price and total:
            price = round(total / quantity, 2)

        product_id = _find_or_create_sale_product(item, location_id)

        create_sale(
            product_id,
            quantity,
            price,
            location_id,
            writeoff_stock=False,
            comment='Продажа импортирована из отчета iiko'
        )

        results.append({
            'name': item.get('name'),
            'quantity': quantity,
            'total': round(quantity * price, 2),
            'status': 'success',
            'message': 'Добавлено в продажи'
        })

    return results

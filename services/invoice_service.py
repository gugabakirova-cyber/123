from models.products import get_products, create_product
from models.stock import add_stock


def _normalize_name(value):
    return str(value or '').lower().strip()


def income_by_invoice_items(items, location_id=None):
    """Оприходует товары из накладной на выбранный склад."""
    results = []
    products = get_products(location_id=location_id)

    for item in items:
        matched_product = None
        item_name = item.get('name')

        for product in products:
            if _normalize_name(product['name']) == _normalize_name(item_name):
                matched_product = product
                break

        if not matched_product:
            product_id = create_product(
                item_name,
                'Сырье',
                item.get('unit') or 'шт',
                item.get('price') or 0,
                0,
                0,
                5,
                location_id
            )
            products = get_products(location_id=location_id)
            for product in products:
                if product.get('id') == product_id or _normalize_name(product['name']) == _normalize_name(item_name):
                    matched_product = product
                    break

        if matched_product:
            add_stock(
                matched_product['id'],
                item.get('quantity') or 0,
                'Приход по накладной',
                location_id
            )

        results.append({
            'name': item_name,
            'quantity': item.get('quantity') or 0,
            'unit': item.get('unit') or '',
            'status': 'success' if matched_product else 'danger',
            'message': 'Оприходовано' if matched_product else 'Не удалось создать товар'
        })

    return results


def invoice_total(items):
    """Считает сумму накладной: количество × закупочная цена."""
    total = 0
    for item in items:
        total += float(item.get('quantity') or 0) * float(item.get('price') or 0)
    return round(total, 2)

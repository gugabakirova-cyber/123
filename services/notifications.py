from models.products import low_stock_products
from db import fetch_one


def get_notifications(location_id=None):

    notifications=[]

    low_stock = low_stock_products(
        location_id
    )

    for product in low_stock:

        notifications.append({
            'type':'warning',
            'message':
            f"{product['name']} заканчивается ({product['quantity']} {product['unit']})"
        })

    count = len(low_stock)

    if count:

        notifications.insert(
            0,
            {
                'type':'danger',
                'message':
                f'{count} товаров требуют закупки'
            }
        )

    return notifications
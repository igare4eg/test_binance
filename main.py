import random


def create_order(volume, number, amountDif, side, priceMin, priceMax):
    orders = []
    total_volume = 0

    for i in range(number - 1):
        price = random.uniform(priceMin, priceMax)

        min_volume = max(0, (volume - total_volume) / (number - i) - amountDif)
        max_volume = min(volume - total_volume, (volume - total_volume) / (number - i) + amountDif)
        order_volume = random.uniform(min_volume, max_volume)

        order = {
            "side": side,
            "price": price,
            "volume": order_volume
        }
        orders.append(order)
        total_volume += order_volume

    # Последний ордер, чтобы гарантировать сумму равную volume
    last_order_volume = volume - total_volume
    last_order = {
        "side": side,
        "price": random.uniform(priceMin, priceMax),
        "volume": last_order_volume
    }
    orders.append(last_order)

    return orders


# Пример использования функции create_order
order_data = {
    "volume": 10000.0,
    "number": 5,
    "amountDif": 50.0,
    "side": "SELL",
    "priceMin": 200.0,
    "priceMax": 300.0
}

orders = create_order(**order_data)
for order in orders:
    print(order)

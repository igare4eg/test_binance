import random
from binance.client import Client
from decimal import Decimal, ROUND_DOWN
from config import API_KEY, API_SECRET

# Установите значения API-ключей и секретов
# API_KEY = 'your_api_key'
# API_SECRET = 'your_api_secret'

def round_down(value, decimals):
    # Округление значения вниз до указанного количества десятичных знаков
    multiplier = Decimal('10') ** Decimal(str(decimals))
    return (Decimal(str(value)) * multiplier).quantize(Decimal('0.' + '0' * decimals), rounding=ROUND_DOWN) / Decimal(str(multiplier))


def create_order(volume, number, amountDif, side, priceMin, priceMax):
    orders = []
    total_volume = 0

    client = Client(API_KEY, API_SECRET)

    symbol_info = client.get_symbol_info('BTCUSDT')
    lot_size_filter = next(filter(lambda f: f['filterType'] == 'LOT_SIZE', symbol_info['filters']), None)
    min_lot_size = float(lot_size_filter['minQty'])
    max_lot_size = float(lot_size_filter['maxQty'])
    step_size = float(lot_size_filter['stepSize'])

    for i in range(number - 1):
        price = round(random.uniform(priceMin, priceMax), 2)  # Округление цены до 2-х знаков после запятой

        min_volume = max(0, (volume - total_volume) / (number - i) - amountDif)
        max_volume = min(volume - total_volume, (volume - total_volume) / (number - i) + amountDif)
        order_volume = round_down(random.uniform(min_volume, max_volume), int(step_size)) # Округление объема с использованием шага

        # Создание ордера через API Binance
        order = client.create_order(
            symbol='BTCUSDT',
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=order_volume,
            price=price
        )

        # Сохранение информации об ордере
        order_info = {
            "side": side,
            "price": price,
            "volume": order_volume,
            "order_id": order['orderId']
        }
        orders.append(order_info)
        total_volume += order_volume

    # Последний ордер, чтобы гарантировать сумму равную volume
    last_order_volume = volume - total_volume
    last_order_volume = round_down(last_order_volume, step_size)  # Округление объема с использованием шага
    last_order = client.create_order(
        symbol='BTCUSDT',
        side=side,
        type='LIMIT',
        timeInForce='GTC',
        quantity=last_order_volume,
        price=round(random.uniform(priceMin, priceMax), 2)  # Округление цены до 2-х знаков после запятой
    )
    last_order_info = {
        "side": side,
        "price": last_order['price'],
        "volume": last_order_volume,
        "order_id": last_order['orderId']
    }
    orders.append(last_order_info)

    return orders

# Пример использования
volume = 10000.0
number = 5
amountDif = 50.0
side = "SELL"
priceMin = 200.0
priceMax = 300.0

orders = create_order(volume, number, amountDif, side, priceMin, priceMax)
print(orders)

import random
from main import create_order

def test_create_order():
    # Тестирование генерации ордеров с правильной суммой объемов
    volume = 10000.0
    number = 5
    amountDif = 50.0
    side = "SELL"
    priceMin = 200.0
    priceMax = 300.0

    orders = create_order(volume, number, amountDif, side, priceMin, priceMax)

    # Проверка суммы объемов ордеров
    total_volume = sum(order["volume"] for order in orders)
    assert total_volume == volume

    # Проверка количества ордеров
    assert len(orders) == number

    # Проверка стороны торговли
    assert all(order["side"] == side for order in orders)

    # Проверка цены ордеров
    assert all(priceMin <= order["price"] <= priceMax for order in orders)

    # Проверка разброса объема каждого ордера
    for i in range(number - 1):
        order_volume = orders[i]["volume"]
        next_order_volume = orders[i+1]["volume"]
        assert abs((order_volume - next_order_volume) / order_volume) <= amountDif / 100

    # Проверка последнего ордера, чтобы сумма объемов равнялась volume
    last_order_volume = orders[-1]["volume"]
    assert abs(sum(order["volume"] for order in orders[:-1]) + last_order_volume - volume) <= 1e-6

# Запуск тестов
if __name__ == '__main__':
    test_create_order()

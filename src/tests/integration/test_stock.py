from src.api.method.stock.stock_main import stock


def test_stock():
    """Тест получение текущих данных с биржи."""
    test_value = stock('/stock SBER')
    assert test_value != 0


def test_stock_not_emit():
    """Тест получение текущих данных с биржи нет эмитента."""
    test_value = stock('/stock NONAME')
    print(test_value)
    assert test_value == 'акции эмитента /stock NONAME не обнаружены в базе Московкой биржи'

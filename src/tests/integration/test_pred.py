from src.api.method.predict.predict_main import predict


async def test_predict():
    """Тест прогноза цен blue chips."""
    test_value = await predict('/predict SBER')
    assert test_value != 0


async def test_predict_wrong():
    """Тест прогноза цен."""
    test_value = await predict('/predict')
    assert test_value == 'Не верный запрос'


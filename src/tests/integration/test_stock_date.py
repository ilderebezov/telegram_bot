import pytest
from src.api.method.stock_date.stock_date_main import stock_date


def test_stock_date():
    """Тест получение истории котировок эмитента с биржи."""
    test_value = stock_date('/stock SBER 2021-12-10')
    assert test_value != 0


def test_stock_date_not():
    """Тест получение истории котировок эмитента с биржи выходной."""
    test_value = stock_date('/stock SBER 2021-12-11')
    print('@@@@@@', test_value)
    assert test_value == 'Акции эмитента SBER не обнаружены в базе Московкой биржи или выбранная дата выходной'

from datetime import datetime, timedelta
def get_dates():
    date_format = '%Y-%m-%d'
    today = datetime.now()
    tomorrow = today + timedelta(days=+1)
    return {'today': today.strftime(date_format),
            'tomorrow': tomorrow.strftime(date_format)}


case_one = '/stock SBER 10-11-2020'
case_one_answer = 'не верный формат даты'
case_two = '/stock SBER' + ' ' + get_dates()['tomorrow']
case_two_answer = 'дата больше вчерашней'
case_three = '/stock SBER' + ' ' + '2009-10-10'
case_three_answer = 'дата меньше 2000-01-01'


@pytest.mark.parametrize("test_input, expected", [(case_one, case_one_answer), (case_two, case_two_answer),
                                                  (case_three, case_three_answer)])
def test_stock_check_date(test_input, expected):
    """Тест получение формата ввода даты."""
    assert stock_date(test_input) == expected

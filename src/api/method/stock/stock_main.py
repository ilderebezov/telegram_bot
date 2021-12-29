import requests


def stock(issuer_name):
    """Получение текущих данных с биржи."""
    url = 'https://iss.moex.com/iss/engines/stock/markets/shares/securities/'
    url += str(issuer_name)
    url += '.json?iss.meta=off'
    request = requests.get(url)
    if request.status_code == 200:
        if len(request.json()['securities']['data']) == 0:
            return f'акции эмитента {str(issuer_name)} не обнаружены в базе Московкой биржи'
        else:
            full_name = request.json()['securities']['data'][0][2]
            price_now = request.json()['marketdata']['data'][0][2]
            if price_now is None:
                return 'Текущий день выходной или данные не доступны'
            return f'акции эмитента {str(issuer_name)} (полное наименование: {full_name}) сейчас стоят {price_now} рублей'
    else:
        return 'неверный запрос, попробуйте еще раз'

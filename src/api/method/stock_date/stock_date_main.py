import requests
import datetime


def validate_date(date_text):
    """Провека даты."""
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return True
    return False


def stock_date(message):
    """Получение истории котировок эмитента с биржи."""
    issuer_name = message.split()[1]
    request_date = message.split()[2]
    now = datetime.datetime.now()
    if validate_date(request_date):
        return 'не верный формат даты'
    elif datetime.datetime.strptime(request_date, '%Y-%m-%d') > now - datetime.timedelta(days=1):
        return 'дата больше вчерашней'
    elif datetime.datetime.strptime(request_date, '%Y-%m-%d') < datetime.datetime.strptime('2010-01-12', '%Y-%m-%d'):
        return 'дата меньше 2000-01-01'
    else:
        url = 'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/tqbr/securities/'
        url += str(issuer_name)
        url += '.json?from=' + str(request_date)
        url += '&till=' + str(request_date)
        request = requests.get(url)
        if request.status_code == 200:
            if len(request.json()['history']['data']) == 0:
                return f'Акции эмитента {str(issuer_name)} не обнаружены в базе Московкой биржи или выбранная ' \
                       f'дата выходной'
            else:
                full_name = request.json()['history']['data'][0][2]
                price = request.json()['history']['data'][0][11]
                return f'Акции эмитента {str(issuer_name)} (полное имя: {full_name}) на дату {request_date} стоили ' \
                       f'{price} рублей'
        else:
            return 'Попробуйте другой запрос, введенныя дата выходной или данные не доступны'

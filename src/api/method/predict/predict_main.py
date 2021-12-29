import asyncio
import datetime
import requests
import os
import pandas as pd

from src.api.db.blue_chips import blue_chips
from src.api.db.db import blue_chips_db
from src.api.method.predict.model import data_model


async def predict(message):
    """Управляющая функция для прогнозирования."""
    if len(message.split()) == 2:
        issuer_name = message.split()[1]
        if issuer_name in blue_chips:
            loop = asyncio.get_event_loop()
            db_blue_ship = await loop.create_task(blue_chips_db(issuer_name))
            return f'прогноз стоимoсти акций эмитента {issuer_name} на следующие 5 дней: ' \
                   f'{data_model(db_blue_ship).to_string(index=False, header=None)}'
        else:
            yesterday = datetime.datetime.now() - datetime.timedelta(1)
            days_delta = datetime.timedelta(days=10)
            earlier_date = yesterday - days_delta
            url = 'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/tqbr/securities/'
            url += str(issuer_name)
            url += '.csv?from=' + earlier_date.strftime('%Y-%m-%d')
            url += '&till=' + yesterday.strftime('%Y-%m-%d')
            request = requests.get(url)
            script_dir = os.path.dirname(__file__)
            file_path = os.path.join(script_dir, 'data.csv')
            with open(file_path, 'wb') as file_db_tmp:
                file_db_tmp.write(request.content)
            data_request = pd.read_csv(file_path, sep=';', encoding='cp1251', skiprows=[0])
            data_request = data_request[['TRADEDATE', 'CLOSE']]
            data_request['dates'] = pd.to_datetime(data_request['TRADEDATE'], dayfirst=True)
        return f'прогноз стоимoсти акций эмитента {issuer_name} на следующие 5 дней: {data_model(data_request).to_string(index=False, header=None)} '
    return 'Не верный запрос'

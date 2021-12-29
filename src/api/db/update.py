
import asyncpg
import datetime
import os
import requests
import pandas as pd
from src.api.db.const import password
from src.api.db.blue_chips import blue_chips


async def update_db():
    """Функция обновления БД."""
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    days_delta = datetime.timedelta(days=20)
    earlier_date = yesterday - days_delta
    full_data = pd.DataFrame()
    for name in blue_chips:
        url = 'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/tqbr/securities/'
        url += str(name)
        url += '.csv?from=' + earlier_date.strftime('%Y-%m-%d')
        url += '&till=' + yesterday.strftime('%Y-%m-%d')
        request = requests.get(url)
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'update_db.csv')
        with open(file_path, 'wb') as file_db_tmp:
            file_db_tmp.write(request.content)
        data_request = pd.read_csv(file_path, sep=';', encoding='cp1251', skiprows=[0])
        data_request = data_request[['TRADEDATE', 'CLOSE']]
        full_data['TRADEDATE'] = data_request[['TRADEDATE']]
        full_data[name] = data_request[['CLOSE']]
    conn = await asyncpg.connect(f"postgres://derebezov:{password}@141.101.178.3:2345/shift_db")
    async with conn.transaction():
        await conn.fetch("TRUNCATE blue_chips RESTART IDENTITY;")
    index_id = 0
    for index, row in full_data.iterrows():
        index_id += 1
        datetime_format = datetime.datetime.strptime(row[0], '%Y-%m-%d')
        async with conn.transaction():
            await conn.executemany('''
                INSERT INTO blue_chips (id, TRADEDATE, GAZP, GMKN, MGNT, MTSS, NLMK, PLZL,
                POLY, ROSN, SBER, SNGS, TATN, TCSG, YNDX)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15);
             ''', [(index_id, datetime_format, str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]), str(row[7]), str(row[8]), str(row[9]), str(row[10]), str(row[11]), str(row[12]), str(row[13]))])
    return 'end_update'

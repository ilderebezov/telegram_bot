"""Функция для получения данных из базы."""

import asyncio
import asyncpg
import datetime
import re
import pandas as pd

from src.api.db.const import password
from src.api.db.update import update_db


async def read_db():
    """Чтение данных из БД."""
    conn = await asyncpg.connect(f"put here your remote DB call")
    async with conn.transaction():
        db_data = await conn.fetch("select json_agg(blue_chips) from blue_chips")
        db_data = db_data[0][0]
        db_out = []
        for item_db in db_data.split():
            dict_line = {}
            for item_in in item_db.split(','):
                item_in_split = item_in.split(':')
                if len(item_in_split) == 2:
                    key = re.sub("[^A-Za-z0-9.-]", "", item_in_split[0])
                    value_db = re.sub("[^A-Za-z0-9.-]", "", item_in_split[1])
                    dict_line[key.upper()] = value_db
            db_out.append(dict_line)
    return db_out


async def blue_chips_db(issuer_name):
    """Чтения данных голубых фишек."""
    db_read = await read_db()
    last_date_in_base = datetime.datetime.strptime(db_read[int(len(db_read) - 1)]['TRADEDATE'], '%Y-%m-%d')
    trade_date = []
    price_line = []
    if (datetime.datetime.now() - last_date_in_base).days > 1:
        await update_db()
        update_db_read = await read_db()
        for line_in_db in update_db_read:
            trade_date.append(datetime.datetime.strptime(line_in_db['TRADEDATE'], '%Y-%m-%d'))
            price_line.append(line_in_db[issuer_name])
        df_out = pd.DataFrame()
        df_out['dates'] = trade_date
        df_out['CLOSE'] = price_line
        return df_out
    for line_in_db in db_read:
        trade_date.append(datetime.datetime.strptime(line_in_db['TRADEDATE'], '%Y-%m-%d'))
        price_line.append(line_in_db[issuer_name])
    df_out = pd.DataFrame()
    df_out['dates'] = trade_date
    df_out['CLOSE'] = price_line
    return df_out

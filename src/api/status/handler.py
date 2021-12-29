import asyncio
from aiohttp import web
import telepot

from src.api.method.predict.predict_main import predict
from src.api.method.stock.stock_main import stock
from src.api.status.schemas import InSchema
from src.api.status.data import TOKEN
from src.api.method.stock_date.stock_date_main import stock_date


routes = web.RouteTableDef()
bot = telepot.Bot(TOKEN)


@routes.post('/')
async def post_handler(request: web.Request) -> web.Response:
    """Получение данных от Телеграм.
    ---
    post:
      description: Получение данных от Телеграм.
      requestBody:
        required: true
        content:
          application/json:
            schema: InSchema
      responses:
        200:
          description: OK
          content:
            application/json:
              schema: InSchema
        422:
          description: Запрос не соответствует схеме.
    """
    request_in = await request.json()
    schema = InSchema()
    request_in = schema.dump(request_in)
    chat_id = request_in['message']['chat']['id']
    message = request_in['message']['text']
    if message == '/start':
        message_rez = 'Бот для получение котировок акций:' \
                      'Телеграм-бот для получение котировок акций с Московской биржи по тикеру акции, ' \
                      'тикер акции можно узнать на https://www.moex.com/.' \
                      ' Принцип работы:' \
                      'По команде /stock <ticker> выводится последняя цена данного тикера. ' \
                      'Пример комманды: /stock AFLT. ' \
                      'По команде /stock <ticker> <date> выводится цена за указанную дату ' \
                      '(формат даты: год-номер месяца-число). Пример комманды: /stock AFLT 2021-09-28. ' \
                      'По комманде /predict <ticker> выводится прогноз стоимости акций эмитента на ближайшие 5 дней, ' \
                      'на базе анализа поведения стоимости акций эмитента за последние 20 дней. ' \
                      'Пример комманды: /predict AFLT '
        bot.sendMessage(chat_id, text=message_rez)
    if '/stock' in message:
        if len(message.split()) == 2:
            message_rez = stock(message.split()[1])
            bot.sendMessage(chat_id, text=message_rez)
        if len(message.split()) == 3:
            message_rez = stock_date(message)
            bot.sendMessage(chat_id, text=message_rez)
    if '/predict' in message:
        try:
            loop = asyncio.get_event_loop()
            message_rez = await loop.create_task(predict(message))
        except Exception:
            message_rez = 'Не верный запрос или ошибка выполнения'
        bot.sendMessage(chat_id, text=message_rez)
    return web.Response(text="Ok")


@routes.get('/get')
async def get_handler(request):
    """Получение данных от Телеграм.
    ---
    get:
      description: test method.
      responses:
        200:
          description: OK
    """
    return web.Response(text="Ok")

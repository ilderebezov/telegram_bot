# telegram bot 

Телеграм-бот для получение котировок акций с Московской биржи по тикеру акции.
@moex_cft_BOT

Принцип работы:
Пользователь запускает бота по команде /start start , ему выводится приветственное сообщение с
описанием команд. По команде /start stock <ticker> выводится последняя цена данного тикера.
По команде /start stock <ticker> <date> выводится цена за указанную дату

Функционал:
- По команде /start выводится приветственное сообщение
- По команде /stock <ticker> выводится последняя цена данного тикера. 
     Пример комманды: /stock AFLT. 
- По команде /stock <ticker> <date> выводится цена за указанную дату 
     (формат даты: год-номер месяца-число). 
      Пример комманды: /stock AFLT 2021-09-28. 
- По комманде /predict <ticker> выводится прогноз стоимости акций эмитента на ближайшие 5 дней
      на базе анализа поведения стоимости акций эмитента за последние 20 дней.
      Пример комманды: /predict AFLT
- Взаимодействие с базой. В базе храняться данные котировок акций "голубых фишек" за последние
20 дней, эти данные испольуются для прогноза стоимости акций "голубых фишек". При запросе
прогноза стоимости акций, на первом этапе опредеяется актуальность базы и в случае 
необходимости база обновляется. После этого происходит расчет прогноза стоимости акции.
В случае если база актуальная происходит чтение данных из базы.

# Разработка

## Рабочее окружение
Для начала разработки необходимо настроить рабочее окружение. Нам понадобятся следующие системные зависимости: 
- [python](https://www.python.org/downloads/) версии 3.9 или выше
- менеджер зависимостей [poetry](https://python-poetry.org/docs/#installation) версии 1.0 или выше

Настройка окружения:
1. Настроить репозиторий
    ```shell script
    git clone git@gitlab.com:shift-python/derebezov/telegram_bot.git
    cd telegram_bot
    ```
2. Установить зависимости. Зависимости установятся в виртуальное окружение.
    ```shell script
    poetry install
    ```

## Запуск

Подключение виртуального окружения
```shell script
poetry shell
```

Из виртуального окружения сервис запускается командой
```shell script
python app.py
```
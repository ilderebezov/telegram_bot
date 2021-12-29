FROM library/python:3.9-slim

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install --no-install-recommends -y build-essential



RUN mkdir -p /telegram_bot
WORKDIR /telegram_bot

COPY . /telegram_bot

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install

EXPOSE 8080
CMD python app.py
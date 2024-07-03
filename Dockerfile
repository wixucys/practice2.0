FROM python:3.12-bullseye

RUN mkdir /tgbot

WORKDIR /tgbot

COPY . .

RUN pip install -r requirements.txt

CMD alembic upgread head && python3 /tgbot/tg-bot/bot.py
FROM python:3.12-bullseye

RUN mkdir /tgbot

WORKDIR /tgbot

COPY . .

RUN pip install -r requirements.txt

CMD alembic upgrade head && python3 /tgbot/tgbot/bot.py
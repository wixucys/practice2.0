FROM python:3.10-bullseye

RUN mkdir /tgbot

WORKDIR /tgbot

COPY . .

RUN pip install -r requirements.txt

CMD /tgbot/tg-bot/bot.py
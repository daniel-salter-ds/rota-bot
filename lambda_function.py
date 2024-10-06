import os
import telebot

from model.rota import Rota
from sheet import Sheet


BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)

sheet = Sheet()
values = sheet.read_values()
rota = Rota(values)
message = str(rota)


def lambda_handler(event, context):
    print('starting')

    if not values:
        bot.send_message(CHAT_ID, text="ERROR: No data found.")
        return

    if len(message) > 4096:
        print(message)
        bot.send_message(CHAT_ID, text=f"Length of message is {len(message)}, exceeding 4096 char limit")
        return

    bot.send_message(CHAT_ID, text=message)

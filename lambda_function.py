import json
import os
import telebot

from datetime import datetime
from model.rota import Rota
from sheet import Sheet


BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)

sheet = Sheet()
values = sheet.read_values()
rota = Rota(values)

def lambda_handler(event, context):
    print('starting')

    if not values:
        bot.send_message(CHAT_ID, text="ERROR: No data found.")
        return

    # Print the entire event for logging purposes
    print("Event: ", event)

    opening = event['opening']

    if opening:
        print("Opening: ", opening)
        message = rota.get_message_by_housemate(date=datetime.now(), opening=opening)
    else:
        message = rota.get_message_by_housemate(date=datetime.now())

    if len(message) > 4096:
        print(message)
        bot.send_message(CHAT_ID, text=f"Length of message is {len(message)}, exceeding 4096 char limit")
        return

    bot.send_message(CHAT_ID, text=message, parse_mode="Markdown")

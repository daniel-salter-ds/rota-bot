import json
import os
from datetime import datetime

import telebot

from model.rota import Rota
from sheet import Sheet

commands = """/start - Start the bot
/rotaRaw - Get all rota data in text format
/rotaLink - Get link to rota sheet
/watco - :)
/help - Show available commands
"""

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

sheet = Sheet()
values = sheet.read_values()
rota = Rota(values)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    start_msg = f"""Howdy housemate, how are you doing?
I'm here to answer all of your rota-related needs!

You can control me by sending these commands:

{commands}"""

    bot.send_message(message.chat.id, start_msg)


@bot.message_handler(commands=['watco'])
def send_time(message):
    bot.send_message(message.chat.id, "Watcooooo")


@bot.message_handler(commands=['rotaRaw'])
def send_raw_rota(message):
    if not values:
        bot.send_message(message.chat.id, "ERROR: No data found.")
        return

    rota = Rota(values)
    bot.send_message(message.chat.id, rota.__str__())

@bot.message_handler(commands=['rotaLink'])
def send_raw_rota(message):
    link = sheet.get_link()

    if not link:
        bot.send_message(message.chat.id, "ERROR: Could not get link to rota sheet.")
        return

    bot.send_message(message.chat.id, link)

@bot.message_handler(commands=['rota'])
def send_rota(message):
    try:
        date_arg = message.text.split()[1]
        date = datetime.strptime(date_arg, "%d/%m/%Y")
    except (IndexError, ValueError):
        date = datetime.now()

    if not values:
        bot.send_message(message.chat.id, "ERROR: No data found.")
        return

    text = rota.get_message_by_housemate(date)
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['id'])
def send_user_id(message):
    file_path = "user_ids.json"

    user = message.from_user
    # user_data = {message.from_user.id: message.from_user.full_name}

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("{}")

    with open(file_path, 'r+') as f:
        existing_data = dict(json.load(f))

        # Update existing data or add new user
        existing_data[user.id] = user.full_name

        # Write updated data back to the JSON file
        f.seek(0)
        f.truncate()
        json.dump(existing_data, f, indent=4)

bot.infinity_polling()

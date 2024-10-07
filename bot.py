import json
import os
import telebot

from datetime import datetime

from model.rota import Rota
from sheet import Sheet

commands = """/start - Start the bot
/rota - Find out who is doing what this week :)
/rotaLink - Get link to rota Google Sheet
/watco - ;)
/help - Show available commands
"""

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

sheet = Sheet()
values = sheet.read_values()
rota = Rota(values)

def save_user_id(message):
    file_path = "user_ids.json"

    user = message.from_user

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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    start_msg = f"""Howdy housemate, how are you doing?
I'm here to answer all of your rota-related needs!

You can control me by sending these commands:

{commands}"""
    save_user_id(message)
    bot.send_message(message.chat.id, start_msg)

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
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['rotaLink'])
def send_rota_link(message):
    link = sheet.get_link()

    if not link:
        bot.send_message(message.chat.id, "ERROR: Could not get link to rota sheet.")
        return

    bot.send_message(message.chat.id, link)

@bot.message_handler(commands=['watco'])
def send_time(message):
    bot.send_message(message.chat.id, "Watcooooo")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, commands)


bot.infinity_polling()

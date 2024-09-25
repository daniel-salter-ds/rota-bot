import os
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
    sheet = Sheet()
    values = sheet.read_values()

    if not values:
        bot.send_message(message.chat.id, "ERROR: No data found.")
        return

    rota = Rota(values)
    bot.send_message(message.chat.id, rota.__str__())

@bot.message_handler(commands=['rotaLink'])
def send_raw_rota(message):
    sheet = Sheet()
    link = sheet.get_link()

    if not link:
        bot.send_message(message.chat.id, "ERROR: Could not get link to rota sheet.")
        return

    bot.send_message(message.chat.id, link)


# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)



bot.infinity_polling()

import os
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def lambda_handler(event, context):
    print('starting')

    bot = telebot.TeleBot(BOT_TOKEN)

    bot.send_message(CHAT_ID, "Sent with <3 from AWS Lambda")

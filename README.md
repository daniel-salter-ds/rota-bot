# rota-bot
A Telegram bot for sending rota reminders.

## Components

1. AWS Lambda function (triggered by AWS Event Bridge)
2. Reads rota data from Google Sheets (via Sheets API)
3. Telegram bot sends this week's tasks to a predetermined group chat (via pyTelegramBotAPI)

import telegram
from telegram.ext import Updater, CommandHandler

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '8189102824:AAHTBq-57_cFp-hOs-iC0yfNeWf_uzFzZFs'
CHAT_ID = '955118357'  # Replace with the chat ID you want to send messages to

def start(update, context):
    context.bot.send_message(chat_id=CHAT_ID, text="Hello, this is a message from your bot!")

def main():
    bot = telegram.Bot(token=BOT_TOKEN)
    # updater = Updater(bot=bot, use_context=True)
    updater = Updater(update_queue=None, bot=bot)
    # dispatcher = updater.

    start_handler = CommandHandler('start', start)
    # dispatcher.add_handler(start_handler)

    updater.start_polling()
    # updater
    # updater.
    # in earlier versions, we were needed to call `idle` here
    # but now, the updater will start the idle loop
    
if __name__ == '__main__':
    main()

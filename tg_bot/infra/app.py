import logging
from typing import List

from telegram import Update
from telegram.ext import BaseHandler, CommandHandler, Application, MessageHandler, filters

FILTER_CATCH_ALL_COMMANDS = filters.COMMAND

FILTER_CATCH_ALL_MESSAGES = filters.TEXT & ~filters.COMMAND

import tg_bot.settings as settings

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)
# log to stderr
logger.addHandler(logging.StreamHandler())

START = "start"

BOT_TOKEN = settings.BOT_TOKEN

def async_callable_wrapper(callback):
    async def async_callable(update: Update, *args, **kwargs):
        message = update.message.text
        response = callback(message)
        await update.message.reply_text(response)
    return async_callable

class App:

    def __init__(self,
                 start_callback: callable =None,
                 help_callback: callable =None):
        self.bot_token = BOT_TOKEN
        self.application: Application = Application.builder().token(self.bot_token).build()

        if start_callback:
            self.add_start_handler(start_callback)

        if help_callback:
            self.add_command_handler("help", help_callback)


    def add_start_handler(self, start_callback):
        self.add_command_handler(START, start_callback)

    def add_command_handler(self, trigger: str, callback: callable):
        self.application.add_handler(CommandHandler(trigger, async_callable_wrapper(callback)))

    def run(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def set_default_message_handler(self, default_message_callback):
        """
        Add a default handler for all messages that do not match any of the registered handlers
        """
        self.application.add_handler(MessageHandler(FILTER_CATCH_ALL_MESSAGES, async_callable_wrapper(default_message_callback)))

    def set_default_command_handler(self, default_command_callback):
        """
        Add a default handler for all commands that do not match any of the registered handlers
        """
        self.application.add_handler(MessageHandler(FILTER_CATCH_ALL_COMMANDS, async_callable_wrapper(default_command_callback)))
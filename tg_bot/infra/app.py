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

        kwargs["message"] = update.message.text
        kwargs["command"] = update.message.text.split()[0]
        kwargs["update"] = update
        kwargs["context"] = args[0]

        kwargs = {k: v for k, v in kwargs.items() if k in set(callback.__code__.co_varnames)}

        # pass the rest of the arguments, but only if they are supported by the callback
        response = callback(**kwargs)
        await update.message.reply_text(response)
    return async_callable

class App:

    default_message_handler = None
    # default_command_handler = None

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
        # if self.default_command_handler:
        #     self.application.add_handler(MessageHandler(FILTER_CATCH_ALL_COMMANDS, self.default_command_handler))

        if self.default_message_handler:
            self.application.add_handler(MessageHandler(FILTER_CATCH_ALL_MESSAGES, self.default_message_handler))

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def set_default_message_handler(self, default_message_callback: callable):
        """
        Add a default handler for all messages that do not match any of the registered handlers
        """
        self.default_message_handler = async_callable_wrapper(default_message_callback)

    # def set_default_command_handler(self, default_command_callback: callable):
    #     """
    #     Add a default handler for all commands that do not match any of the registered handlers
    #     """
    #     self.default_command_handler = async_callable_wrapper(default_command_callback)
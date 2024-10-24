import logging
from typing import List

from telegram import Update
from telegram.ext import BaseHandler, CommandHandler, Application, MessageHandler, filters
from telegram.ext._utils.types import CCT, HandlerCallback, RT

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

def tg_bot_callback(callback) -> HandlerCallback[Update, CCT, RT]:
    async def async_callable_wrapper(update: Update, *args, **kwargs):

        # instead of `message` or `edited_message` use `effective_message`
        # kwargs["message"] = update.message.text
        # kwargs["command"] = update.message.text.split()[0]
        update_text = update.effective_message.text
        kwargs["message"] = update_text
        kwargs["command"] = update_text.split()[0]
        kwargs["command_tail"] = update_text.split()[1:]
        kwargs["update"] = update
        kwargs["context"] = args[0]

        kwargs = {k: v for k, v in kwargs.items() if k in set(callback.__code__.co_varnames)}

        reply_func = None
        announce = ""

        if update.message:
            announce = f"Received message: {update.message.text}"
            logger.info(announce)
            reply_func = update.message.reply_text
        elif update.edited_message:
            announce = f"Received edited message: {update.edited_message.text}"
            logger.info(announce)
            reply_func = update.edited_message.reply_text

        if reply_func:
            await reply_func(announce)
            await reply_func(f"Command: {kwargs['command']}")

        # pass the rest of the arguments, but only if they are supported by the callback
        response = callback(**kwargs)
        await reply_func(response)
    return async_callable_wrapper

class App:

    default_message_handler = None

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
        self.application.add_handler(CommandHandler(trigger, tg_bot_callback(callback)))

    def run(self):
        if self.default_message_handler:
            self.application.add_handler(MessageHandler(FILTER_CATCH_ALL_MESSAGES, self.default_message_handler))

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def set_default_message_handler(self, default_message_callback: callable):
        """
        Add a default handler for all messages that do not match any of the registered handlers
        """
        self.default_message_handler = tg_bot_callback(default_message_callback)

    def command_handler(self, param, *args, **kwargs):
        def decorator(callback):
            self.add_command_handler(param, callback)
            return callback
        return decorator

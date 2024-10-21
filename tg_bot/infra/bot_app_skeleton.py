#!/usr/bin/env python
# pylint: disable=unused-argument
import logging
from typing import List

from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes, BaseHandler)

import tg_bot.settings as settings

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)
# log to stderr
logger.addHandler(logging.StreamHandler())

BOT_TOKEN = settings.BOT_TOKEN
CHAT_ID = settings.CHAT_ID


def main(handlers: List[BaseHandler]) -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    [application.add_command_handler(handler) for handler in handlers]

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends explanation on how to use the bot."""
        await update.message.reply_text("Welcome!")

    main([CommandHandler("start", start)])
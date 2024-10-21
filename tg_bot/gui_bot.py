#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.
import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

import settings

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)
# log to stderr
logger.addHandler(logging.StreamHandler())

BOT_TOKEN = settings.BOT_TOKEN
CHAT_ID = settings.CHAT_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display a button to reply with the user's username."""
    await update.message.reply_text(
        "Press the button to get your username.",
        reply_markup=ReplyKeyboardMarkup([["Get username"]], resize_keyboard=True),
    )

async def get_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the user's username."""
    await update.message.reply_text(f"Your username is {update.effective_user.username}")


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    app = Application.builder().token(BOT_TOKEN).build()

    # Add the command handlers
    app.add_command_handler(CommandHandler("start", start))
    # app.add_handler(CallbackQueryHandler(get_username))
    # Message handler with a regex pattern
    app.add_command_handler(MessageHandler(filters.Regex("Get username"), get_username))

    # Start the Application
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
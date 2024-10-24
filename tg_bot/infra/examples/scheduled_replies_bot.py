#!/usr/bin/env python
# pylint: disable=unused-argument
import logging
from datetime import datetime
from typing import List

from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes, BaseHandler, CallbackContext)

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

    for handler in handlers:
        application.add_handler(handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":

    async def alert(callback_context: CallbackContext, chat_id: int, *args, **kwargs):

        dt = datetime.now()
        msg: str = f"alert is invoked at {dt}"
        logger.debug(msg)
        job = callback_context.job

        await callback_context.bot.send_message(chat_id, text=msg)

    ##################################################################
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends explanation on how to use the bot."""
        await update.message.reply_text("Welcome!")

    async def opt_in(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("subscribing to updates...")

        # async coroutine to wrap alert with chat_id
        chat_id = update.effective_chat.id

        async def alert_wrapper(context):
            await alert(context, chat_id=chat_id)

        context.job_queue.run_repeating(callback=alert_wrapper, interval=10*60)

    main([
            CommandHandler("start", start),
            CommandHandler("optin", opt_in)
        ])

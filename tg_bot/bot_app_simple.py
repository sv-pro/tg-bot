#! /usr/bin/env python
from collections.abc import Callable
from functools import partial
from typing import List, Dict, Coroutine, Any

from telegram.ext import BaseHandler

from infra.bot_app_skeleton import main, CommandHandler


async def async_reply(msg, update):
    await update.message.reply_text(msg)

def reply(msg, update):
    update.message.reply_text(msg)


async def async_wrapper_callback(update, context, callback, *args, **kwargs) -> None:
    """Sends explanation on how to use the bot."""
    msg_raw_text: str = update.message.text
    msg: str = msg_raw_text.split(" ", 1)[1] if len(msg_raw_text.split(" ", 1)) > 1 else ""

    if msg:
        kwargs["msg"] = msg

    msg_reply: str = callback(*args, **kwargs)
    await async_reply(msg_reply, update)

def init_bot(config: Dict[str, Callable]) -> List[BaseHandler]:
    return [CommandHandler(k, partial(async_wrapper_callback, callback=v))
            for k, v in config.items()]

##########################################################
def start() -> str:
    """Sends welcome message."""
    msg: str = "Welcome!"
    return msg

def help() -> str:
    """Sends explanation on how to use the bot."""
    msg: str = "Help!"
    return msg

def echo(msg: str) -> str:
    """Echoes the user message."""
    return msg

##########################################################

if __name__ == "__main__":
    main(init_bot({
        "start": start,
        "help": help,
        "echo": echo
    }))
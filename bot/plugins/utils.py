import os
import shutil
from os import execl
from time import sleep
from sys import executable
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from bot import SUDO_USERS, DOWNLOAD_DIRECTORY, LOGGER, SUPPORT_CHAT_LINK
from bot.config import Messages as tr
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.private & filters.incoming & filters.command(['log']) & filters.user(SUDO_USERS))
def _send_log(client, message):
  with open('log.txt', 'rb') as f:
    try:
      client.send_document(
        message.chat.id,
        document=f,
        file_name=f.name,
        reply_to_message_id=message.message_id
        )
      LOGGER.info(f'Log file sent to {message.from_user.id}')
    except FloodWait as e:
      sleep(e.x)
    except RPCError as e:
      message.reply_text(e, quote=True)

@Client.on_message(filters.private & filters.incoming & filters.command(['restart']) & filters.user(SUDO_USERS))
def _restart(client, message):
  shutil.rmtree(DOWNLOAD_DIRECTORY)
  LOGGER.info('Deleted DOWNLOAD_DIRECTORY successfully.')
  message.reply_text('**♻️Restarted Successfully !**', quote=True)
  LOGGER.info(f'{message.from_user.id}: Restarting...')
  execl(executable, executable, "-m", "bot")

@Client.on_message(filters.private & filters.incoming & filters.command(['about']))
async def _restart(client, message):
    await message.reply_text(
            text=START_TEXT.format(message.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
@Client.on_callback_query()
async def button(bot, update):
    if update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=False
        )

    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=False
        )

    
    else:
        await update.message.delete()

START_TEXT = """
**Hi  {}  I am Google Service Accounts Generator Bot**

Made by @moedyiu
"""

HELP_TEXT = """
**I cannot help you 😌**

Made by @moedyiu
"""
ABOUT_TEXT = """
- **Bot :** `GOOGLE SERVICE ACC GEN BOT`
- **Creator :** [Moedyiu](https://telegram.me/moedyiu)
- **Channel :** [Moedyiu](https://telegram.me/moedyiu)
- **Credits :** `Everyone in this journey`
- **Source :** [Click here](https://github.com/modbots)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram v1.2.0](https://pyrogram.org)
- **Server :** [Heroku](https://heroku.com)
""" 
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
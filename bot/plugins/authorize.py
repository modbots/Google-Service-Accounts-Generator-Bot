import re
import os
import json
from httplib2 import Http
from bot import LOGGER
from json import loads
from bot.config import Messages
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bot.helpers.sql_helper import gDriveDB
from bot.config import BotCommands
from bot.helpers.utils import CustomFilters

SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/cloud-platform','https://www.googleapis.com/auth/iam']
OAUTH_SCOPE = "https://www.googleapis.com/auth/drive"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"
flow = None

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Authorize))
async def _auth(client, message):
  user_id = message.from_user.id
  credentials = 'bot/credentials/' + str(user_id) + '/credentials.json'

  if not os.path.exists(credentials):
    await message.reply_text(Messages.NOT_AUTH, quote=True)
  else:
    G_DRIVE_CLIENT_ID = loads(open(credentials,'r').read())['installed']['client_id']
    G_DRIVE_CLIENT_SECRET = loads(open(credentials,'r').read())['installed']['client_secret']
    
    global flow
    try:
        
        flow = OAuth2WebServerFlow(
                G_DRIVE_CLIENT_ID,
                G_DRIVE_CLIENT_SECRET,
                SCOPES,
                redirect_uri=REDIRECT_URI
        )
        auth_url = flow.step1_get_authorize_url()
        LOGGER.info(f'AuthURL:{user_id}')
        await message.reply_text(
          text=Messages.AUTH_TEXT.format(auth_url),
          quote=True,
          reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Authorization URL", url=auth_url)]]
                )
          )
    except Exception as e:
      await message.reply_text(f"**ERROR:** ```{e}```", quote=True)

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Revoke) & CustomFilters.auth_users)
def _revoke(client, message):
  user_id = message.from_user.id
  try:
    gDriveDB._clear(user_id)
    LOGGER.info(f'Revoke:{user_id}')
    message.reply_text(Messages.REVOKED, quote=True)
  except Exception as e:
    message.reply_text(f"**ERROR:** ```{e}```", quote=True)


@Client.on_message(filters.private & filters.incoming & filters.text & ~CustomFilters.auth_users)
async def _token(client, message):
  token = message.text.split()[-1]
  WORD = len(token)
  if WORD == 62 and token[1] == "/":
    creds = None
    global flow
    if flow:
      try:
        user_id = message.from_user.id
        sent_message = await message.reply_text("🕵️**Checking received code...**", quote=True)
        creds = flow.step2_exchange(message.text)
        gDriveDB._set(user_id, creds)
        LOGGER.info(f'AuthSuccess: {user_id}')
        await sent_message.edit(Messages.AUTH_SUCCESSFULLY)
        flow = None
      except FlowExchangeError:
        await sent_message.edit(Messages.INVALID_AUTH_CODE)
      except Exception as e:
        await sent_message.edit(f"**ERROR:** ```{e}```")
    else:
        await message.reply_text(Messages.FLOW_IS_NONE, quote=True)
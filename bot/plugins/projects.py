import os, pickle
from time import sleep
import logging
from bot.helpers.sql_helper import gDriveDB
from googleapiclient.discovery import build
from pyrogram import Client, filters
from bot.helpers.sagen import _get_projects, _create_projects, _enable_services
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from bot.helpers.utils import CustomFilters
from pyrogram import Client, filters
from bot.config import BotCommands, Messages
from bot.helpers.utils import CustomFilters
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Proj) )
def _pro(client, message):
    user_id = message.from_user.id
    #message.reply_text('🕵️**Checking Credential...**', quote=True)    
    creds =  gDriveDB.search(user_id)
    if creds is None:
         message.reply_text(Messages.NOT_AUTH, quote=True)
    else:
        cloud = build('cloudresourcemanager', 'v1', credentials=creds, cache_discovery=False)
        current_count = len(_get_projects(cloud)) 
        if current_count == 0:
            message.reply_text( "🕵️**You have no project**\n_send /newproject to create one or more projects")
        else:
            get = str(_get_projects(cloud)).replace('[', '').replace(',', '\n').replace(']', '').replace("'", "").replace(" ", "")
            tex ='🕵️**TOTAL CREATED PROJECTS**: {} \n\n'.format(current_count)
            tex2 = ''
            message.reply_text( tex + get + tex2 )
        
    
@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Cproj) )
def _Cpro(client, message):
    user_id = message.from_user.id
    
    if len(message.command) > 1:
        num = message.command[1]
        try:
            number = int(num)
            
            creds =  gDriveDB.search(user_id)
            serviceusage = build('serviceusage','v1',credentials=creds, cache_discovery=False)
            services=['iam','drive']
            if creds is None:
                message.reply_text(Messages.NOT_AUTH, quote=True)
            else:
                cloud = build('cloudresourcemanager', 'v1', credentials=creds, cache_discovery=False)
                current_count = len(_get_projects(cloud))
                
                if current_count + number <= 12:
                    projects = _create_projects(cloud, number)
                    message.reply_text('🕵️**NEWLY CREATED*** \n\n' + str(projects).replace('[', '').replace(',', '\n').replace(']', '').replace("'", "") , quote=True)  
                    ste = _get_projects(cloud)
                    services = [i + '.googleapis.com' for i in services]
                    enable = _enable_services(serviceusage,ste,services)
                    
                else:
                    remaining = 12 - current_count
                    if remaining == 0:
                        message.reply_text('🕵️**You Can NOT CREATE ANY MORE**', quote=True) 
                    else:
                        message.reply_text('🕵️**You Can Only Create ' + str(remaining) + " more projects**", quote=True) 
        except ValueError:
            message.reply_text('🕵️**Please Give value as Number**\n_send /newproject 3', quote=True)
    else:
        message.reply_text('🕵️**Please Give me Some value**\n_send /newproject 3', quote=True) 

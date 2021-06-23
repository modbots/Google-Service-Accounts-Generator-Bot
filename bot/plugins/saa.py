import os, pickle
import googleapiclient.discovery
import pathlib
import ast
import shutil
from shutil import copytree, rmtree
from base64 import b64decode
from json import dumps, dump, loads, load
from time import sleep
from bot.helpers.sql_helper import gDriveDB
from googleapiclient.discovery import build
from pyrogram import Client, filters
from bot.helpers.sagen import _create_remaining_accounts, _batch_keys_resp, _list_sas, _create_sa_keys, _delete_sas
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from bot.helpers.utils import CustomFilters
from pyrogram import Client, filters
from bot.config import BotCommands, Messages
from bot.helpers.utils import CustomFilters
from math import remainder


@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Delsas) )
def _del(client, message):
    user_id = message.from_user.id
    sentmessage = message.reply_text('🕵️** Checking...**', quote=True)   
    creds =  gDriveDB.search(user_id)
    if len(message.command) > 1:
        project = message.command[1]
        projects = [project]
        if creds is None:
           sentmessage.edit(Messages.NOT_AUTH, quote=True)
        
        else:
            #cloud = build('cloudresourcemanager', 'v1', credentials=creds)
            iam = build('iam', 'v1', credentials=creds, cache_discovery=False)
            for i in projects:
                deleteing = _delete_sas(iam,i)

            sentmessage.edit('FINISHED DELETING')

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Sas) )
def _sas(client, message):
    user_id = message.from_user.id
    sentmessage = message.reply_text('🕵️**Checking...**', quote=True)    
    creds =  gDriveDB.search(user_id)
    patha = "bot/credentials/" + str(user_id) + '/'
    if len(message.command) > 1:
        project = message.command[1]
        projects = [project]
        if creds is None:
           sentmessage.edit(Messages.NOT_AUTH, quote=True)
        
        else:
            #cloud = build('cloudresourcemanager', 'v1', credentials=creds)
            iam = build('iam', 'v1', credentials=creds, cache_discovery=False)
            prefix = "mfc-"
            sentmessage.edit('Building Sas')
            SAS = _create_remaining_accounts(iam,project)
            GEN =_generate_keys(project, prefix, creds, sentmessage, patha)
            sentmessage.edit('SA GENERATION WAS FINISHED')
            with open(patha + "/sas-list.txt", 'rb') as f:
               client.send_document(document=f,
                                    chat_id=user_id,
               )
            shutil.make_archive(project, 'zip', patha)
            with open(project + ".zip", 'rb') as z:
               client.send_document(document=z,
                                    chat_id=user_id,
               )
            #src = os.path.join(os.getcwd(), patha)
            #dst = os.path.join(os.getcwd(), 'bot/accounts/' + str(user_id))
            #copytree(src, dst, dirs_exist_ok=True)
            #rmtree(src, ignore_errors=True)
            shutil.rmtree(patha)
            os.remove(project + ".zip")
            
    else:
        message.reply_text(Messages.NOT_AUTH, quote=True)
    

def _generate_keys(project_id, prefix, creds, sentmessage, patha):
    total_sas = list_service_accounts(project_id, creds)['accounts']
    prefix_sas=[]
    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=creds, cache_discovery=False)
    print("Length of sas =", len(total_sas))
    for account in total_sas:
        # print("%s, prefix=%s" %(account['displayName'],account['displayName'][0:3]))
        if(account['displayName'][0:len(prefix)]==prefix):
            prefix_sas.append(account)

    print("Length of {} sas =".format(prefix), len(prefix_sas))

    i=0
    sas_list_string = ""
    if not os.path.exists(patha):
        os.mkdir(patha)
    sas_list = open(patha + 'sas-list.txt', 'w+')
    sas_list.close()
    for sas in prefix_sas:
        sas_list = open(patha + 'sas-list.txt', 'a')
        sas_list_string+=str(sas['email'])+"\n"
        # print(i)
        if (remainder(i,10)==-1):
            sas_list_string+="\n"
            i=0
        else:
            i+=1
        sas_list.write(sas_list_string)
        sas_list_string = ""
        response = create_key(sas['email'], service, sentmessage)
        # print("\n\n\n",response['privateKeyData'],"\n\n\n")
        key_dump = {"name":response['name'][response['name'].rfind('/'):], "data":ast.literal_eval(b64decode(response['privateKeyData']).decode('utf-8'))}
        # print(key_dump["data"])
        with open(patha + '%s.json' % (key_dump["name"]), 'w+') as f:
            f.write(dumps(key_dump['data'], indent = 2))

def list_service_accounts(project_id, creds):
    """Lists all service accounts for the current project."""

    credentials = creds
    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials, cache_discovery=False)

    service_accounts = service.projects().serviceAccounts().list(
        name='projects/' + project_id, pageSize=100).execute()

    # for account in service_accounts['accounts']:
    #     print('Name: ' + account['name'])
    #     print('Email: ' + account['email'])
    #     print(' ')
    return service_accounts

def create_key(service_account_email, service, sentmessage):
    """Creates a key for a service account."""
    
    tex ='\n\nWE ARE GENERATING AND PLEASE WAIT!\n\n'
    tex2 = '\n\n@moedyiu'

    sentmessage.edit(tex + str(service_account_email) + tex2)
    key = service.projects().serviceAccounts().keys().create(
        name='projects/-/serviceAccounts/' + service_account_email, body={}
        ).execute()
    

    # print('Created key: ' + key['name'])
    return key

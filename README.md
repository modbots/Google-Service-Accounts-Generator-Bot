# Google Srvice Accounts Generator Telegram Bot
**A Telegram bot to generate google service accounts.**
- Find it on Telegram as [Google Service Accounts](https://t.me/GoogleSA_Bot)

## Features
- [X] Create New Projects.
- [X] Generate Service Accounts.
- [X] Delete Service Accounts.
- [X] Extract Service Mails.


## ToDo 
- [ ] Handle more exceptions.
- [ ] LOGGER support.
- [ ] Update command.

## Deploying

### Deploy on [Heroku](https://heroku.com)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/modbots/Google-Service-Accounts-Generator-Bot/tree/master)

### Installation

- Clone this git repository.
```sh 
git clone https://github.com/modbots/Google-Service-Accounts-Generator-Bot
```
- Change Directory
```sh 
cd Google-Service-Accounts-Generator-Bot
```
- Install requirements with pip3
```sh 
pip3 install -r requirements.txt
```

### Configuration
**There are two Ways for configuring this bot.**
1. Add values to Environment Variables. And add a `ENV` var to Anything to enable it.
2. Add values in [config.py](./bot/config.py). And make sure that no `ENV` environment variables existing.

### Configuration Values
- `BOT_TOKEN` - Get it by contacting to [BotFather](https://t.me/botfather)
- `APP_ID` - Get it by creating app on [my.telegram.org](https://my.telegram.org/apps)
- `API_HASH` - Get it by creating app on [my.telegram.org](https://my.telegram.org/apps)
- `SUDO_USERS` - List of Telegram User ID of sudo users, seperated by space.
- `SUPPORT_CHAT_LINK` - Telegram invite link of support chat.
- `DATABASE_URL` - Postgres database url.
- `DOWNLOAD_DIRECTORY` - Custom path for downloads. Must end with a forward `/` slash. (Default to `./downloads/`)

### Deploy 
```sh 
python3 -m bot
```

## Credits
- [Dan](https://github.com/delivrance) for creating [PyroGram](https://pyrogram.org)
- [Spechide](https://github.com/Spechide) for [gDriveDB.py](./bot/helpers/sql_helper/gDriveDB.py)
- [xyou365](https://github.com/xyou365/AutoRclone) for Autorclone
## Copyright & License
- Copyright (©) 2021 by [Moedyiu](https://github.com/modbots)
- Licensed under the terms of the [GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007](./LICENSE)

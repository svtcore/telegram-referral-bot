# Telegram Referral Bot
Help to add telegram accounts with referral code to bots which have referral system 

## Installation
```
pip install -r requirements.txt
```

## Setup

### 1. Open .env file and edit values

Description for fileds

**BOT_NAME** - public name of bot without @ symbol (example_random_bot)

**COUNT** - quantity of account which will be used

**REFER_ID** - your referal ID which you got from bot (t.me/example_random_bot?start=12345 , set ONLY 12345)

**JOIN_CHANNEL** - enabled/disable function to join channel bot if it's required. Default is 0, to enable set 1 [OPTIONAL]

**CHANNEL_NAME** - username of channel which must to be joined. Works when **JOIN_CHANNEL** is set 1 [OPTIONAL]

**DELAY_MIN** - minimum delay in seconds between working each account

**DELAY_MAX** - maximum delay in seconds between working each account

**AUTH** - set 1 if you don't have sessions files in folder ./sessions otherwise 0

**RUN** - set 1 if you have session files and want start script  

### 2. Put tokens into file tokens.txt in format
```
session_name:API_ID:API_HASH
#example
my_session_1:9863729:dc5795b76bdc05e1e6c653742c5ba530
```
(How get API_ID and API_HASH follow https://my.telegram.org autorize, create application and you will get credentials)

### 3. Put proxies into file proxy.txt
There are 3 diffrent format for proxies (ONLY SOCKS5)
```
NO PROXY (leave file empty)
IP:PORT
IP:PORT:LOGIN:PASSWORD
```

If you don't have session files in folder **sessions** you must set params AUTH=1 , RUN=1, otherwise  AUTH=0, RUN=1

### 4. Run file bot.py

```
python bot.py
```
### 5. After run script you should autorize on each account then you will get session files into folder sessions and bot starts add with your referal code

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://github.com/svtcore/telegram-referral-bot/blob/main/LICENSE)

## Involved libraries
* [Pyrogram](https://github.com/pyrogram/pyrogram)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

## Responsibility
All materials are provided for educational purposes only. The author does not bear the responsibility of the consequences of use by other users

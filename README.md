## Telegram Referral Bot
### ***Script to add Telegram accounts as referrals to bots, using your invite code***
It emulates the **/start** command to the bot with an additional parameter for the referral code.

![Screenshoot](https://github.com/svtcore/telegram-referral-bot/blob/main/screenshot.png)

### 1. Install necessary libraries
```
pip install -r requirements.txt
```
### 2. Open the .env file and edit the data according to your needs
Description for fileds
 - **BOT_NAME** - The public name of the bot without the @ symbol (e.g., example_random_bot)
 - **COUNT** - The quantity of accounts to be used
 - **REFER_ID** - Your referral ID obtained from the bot (e.g., t.me/example_random_bot?start=12345, ONLY set 12345)
 - **CHANNEL_NAME** - The username of the channel that must be joined [OPTIONAL]
 - **DELAY_MIN** - The minimum delay in seconds between each account's operation
 - **DELAY_MAX** - The maximum delay in seconds between each account's operation


Example of **.env** file
```
BOT_NAME=my_new_coin_bot
COUNT=5
REFER_ID=111222333
CHANNEL_NAME=my_new_coin_channel
DELAY_MIN = 10
DELAY_MAX = 15
```
### 2.1 If you use pyrogram string sessions, follow steps: [4](https://github.com/svtcore/telegram-referral-bot?tab=readme-ov-file#4-create-a-file-for-your-credentials-such-as-accountstxt-and-input-the-data-in-the-following-format) ,[5](https://github.com/svtcore/telegram-referral-bot?tab=readme-ov-file#5-if-you-plan-to-use-a-proxy-create-a-file-for-it-in-this-format) and [8](https://github.com/svtcore/telegram-referral-bot?tab=readme-ov-file#8-run-the-script-to-begin-inviting-accounts-using-your-referral-code)
### 3. Retrieve the API_ID and API_HASH for each account
 - Go to https://my.telegram.org. Log in to the site and create a new application; it will provide you with your credentials
### 4. Create a file for your credentials, such as accounts.txt, and input the data in the following format:

Note: The amount of tokens must correspond to the amount you have set in the **.env** file.

Example
```
SESSION_NAME:API_ID:API_HASH
MY_ACCOUNT_1:11223344:d54d1702ad0f8326224b817c796763c9
```
Or if you've got pyrogram string sessions, just pop each one on a new line like this:
```
Ag1C11H4AJxbIL5Cr4xovee6MlhrE0XYJud9h_w4RbADPko_-BQufNvWzAzci_4_1EEv623CFNTqRhlL_4qnwL_C3SuMRXYgR89LOSjbE8YO8yIiA0Dctyt5BwdinvMFFm6CEqhzhMzFXoqwCjAMCF9BWkUdJ0WqXkUjxkWO68rJXRIDLl2PXqEGOijZRLnVQIf2H8oJAuAe8Wo7nfYFuFQJAJH7CvpFiY2VZWeBVjSrgWspbTY3Kiy5q7EBrkHFeZvF5y5N_fWnkrAAWYmLN2zctOLuRm2SJ2DQ2mzZdYjKs4Dxzu1QeHTnRdnDCgE9SjEp2C3RFioZDy38105ao_da6owAAAAB3o_RZAA
Ag2C21H4AJxbIL5Cr4xovee6MlhrE0XYJud9h_w4RbADPko_-BQufNvWzAzci_4_1EEv623CFNTqRhlL_4qnwL_C3SuMRXYgR89LOSjbE8YO8yIiA0Dctyt5BwdinvMFFm6CEqhzhMzFXoqwCjAMCF9BWkUdJ0WqXkUjxkWO68rJXRIDLl2PXqEGOijZRLnVQIf2H8oJAuAe8Wo7nfYFuFQJAJH7CvpFiY2VZWeBVjSrgWspbTY3Kiy5q7EBrkHFeZvF5y5N_fWnkrAAWYmLN2zctOLuRm2SJ2DQ2mzZdYjKs4Dxzu1QeHTnRdnDCgE9SjEp2C3RFioZDy38105ao_da6owAAAAB3o_RZAA
Ag3C31H4AJxbIL5Cr4xovee6MlhrE0XYJud9h_w4RbADPko_-BQufNvWzAzci_4_1EEv623CFNTqRhlL_4qnwL_C3SuMRXYgR89LOSjbE8YO8yIiA0Dctyt5BwdinvMFFm6CEqhzhMzFXoqwCjAMCF9BWkUdJ0WqXkUjxkWO68rJXRIDLl2PXqEGOijZRLnVQIf2H8oJAuAe8Wo7nfYFuFQJAJH7CvpFiY2VZWeBVjSrgWspbTY3Kiy5q7EBrkHFeZvF5y5N_fWnkrAAWYmLN2zctOLuRm2SJ2DQ2mzZdYjKs4Dxzu1QeHTnRdnDCgE9SjEp2C3RFioZDy38105ao_da6owAAAAB3o_RZAA
```
### 5. If you plan to use a proxy, create a file for it in this format:
```
NO PROXY (leave file empty)
IP:PORT
IP:PORT:LOGIN:PASSWORD
```
### 6. Create session files and authorize on each account
```
python bot.py --auth --tokens accounts.txt
```
### 7. After authorization is complete, session files will be generated in the 'sessions' folder
### 8. Run the script to begin inviting accounts using your referral code
```
python bot.py --run --tokens accounts.txt
```
or with string session
```
python bot.py --run --strings --tokens accounts.txt
```
or with proxy
```
python bot.py --run --tokens accounts.txt --proxies proxies.txt
```
If the bot requires joining a channel, you should set up the channel name in the **.env** file and follow the command below
```
python bot.py --run --tokens accounts.txt --channel
```
Note: All files, such as **accounts.txt** and **proxies.txt**, must be located in the root of the project folder

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 
If the script returns an error, open an issue with the provided error message 

## License
[MIT](https://github.com/svtcore/telegram-referral-bot/blob/main/LICENSE)

## Involved libraries
* [Pyrogram](https://github.com/pyrogram/pyrogram)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

## Responsibility
All materials are provided for educational purposes only. The author does not bear the responsibility of the consequences of use by other users

from classes.main import Main
from classes.auth import Auth
from dotenv import load_dotenv
import os

load_dotenv()

BOT_NAME = os.getenv('BOT_NAME')
COUNT = os.getenv('COUNT')
REFER_ID = os.getenv('REFER_ID')
DELAY_MIN = os.getenv('DELAY_MIN')
DELAY_MAX = os.getenv('DELAY_MAX')
JOIN_CHANNEL = os.getenv('JOIN_CHANNEL')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
AUTH = os.getenv('AUTH')
RUN = os.getenv('RUN')


bot = Main(BOT_NAME, COUNT, JOIN_CHANNEL, CHANNEL_NAME, DELAY_MIN, DELAY_MAX, REFER_ID)
bot.check_sessions_folder()
auth = Auth()
if (int(AUTH) != 0):
    auth.start()
if (int(RUN) != 0):
    bot.start()
    print("Done")

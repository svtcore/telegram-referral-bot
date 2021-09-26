from pyrogram import Client
from pyrogram.raw import functions
from classes.main import Main
from classes.auth import Auth

BOT_NAME = "sample_bot"
COUNT = 5
REFER_ID = "12345"
DELAY_MIN = 2
DELAY_MAX = 5


bot = Main(BOT_NAME, COUNT, DELAY_MIN, DELAY_MAX, REFER_ID)
auth = Auth()
auth.start()
bot.start()

import os
import logging
from dotenv import load_dotenv
from classes.main import Main
from classes.auth import Auth

# Load environment variables from .env file
load_dotenv()

# Define logging format
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Read environment variables
BOT_NAME = os.getenv('BOT_NAME', '')
COUNT = int(os.getenv('COUNT', 0))
REFER_ID = os.getenv('REFER_ID', '')
DELAY_MIN = int(os.getenv('DELAY_MIN', 0))
DELAY_MAX = int(os.getenv('DELAY_MAX', 0))
AUTH = int(os.getenv('AUTH', 0))
RUN = int(os.getenv('RUN', 0))

# Validate environment variables
if not BOT_NAME:
    raise ValueError("BOT_NAME is missing in environment variables")
if not REFER_ID:
    raise ValueError("REFER_ID is missing in environment variables")
if DELAY_MIN > DELAY_MAX:
    raise ValueError("DELAY_MIN cannot be greater than DELAY_MAX")

# Create objects for Main and Auth
bot = Main(BOT_NAME, COUNT, DELAY_MIN, DELAY_MAX, REFER_ID)
auth = Auth()

# Start the authorization process if AUTH is not 0
if AUTH != 0:
    try:
        auth.start()
    except Exception as e:
        logger.error(f"Error starting authorization process: {e}")

# Start the bot if RUN is not 0
if RUN != 0:
    try:
        bot.start()
        logger.info("Bot started successfully")
    except Exception as e:
        logger.error(f"Error starting the bot: {e}")

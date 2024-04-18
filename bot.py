from classes.main import Main
from classes.auth import Auth
from dotenv import load_dotenv
import os
import argparse
import sys

load_dotenv()

BOT_NAME = os.getenv('BOT_NAME')
COUNT = os.getenv('COUNT')
REFER_ID = os.getenv('REFER_ID')
DELAY_MIN = os.getenv('DELAY_MIN')
DELAY_MAX = os.getenv('DELAY_MAX')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
JOIN_CHANNEL = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process command line arguments")
    parser.add_argument("-a", "--auth", action="store_true", help="Flag to start authentication")
    parser.add_argument("-r", "--run", action="store_true", help="Flag to run bot")
    parser.add_argument("-ch", "--channel", action="store_true", help="Flag to enable join to channel")
    parser.add_argument("-t", "--tokens", type=str, help="Name of the file to load tokens")
    parser.add_argument("-p", "--proxies", type=str, help="Name of the file to load proxies")
    args = parser.parse_args()
    if args.channel:
        JOIN_CHANNEL = True
    if args.tokens:
        bot = Main(BOT_NAME, COUNT, JOIN_CHANNEL, CHANNEL_NAME, DELAY_MIN, DELAY_MAX, REFER_ID, args.tokens, args.proxies)
        bot.check_sessions_folder()
        if args.auth:
            auth = Auth(args.tokens, args.proxies)
            auth.start()
        if args.run:
            bot.start()
        if not args.auth and not args.run:
            parser.error("At least one of --auth or --run must be provided")
            sys.exit(1)
    else:
        print("Error: File with tokens not specified.")
        print("Please specify the file containing tokens using the -t or --tokens option.")
        sys.exit(1)
    print("Done")

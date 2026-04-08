from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Pyrogram requires an event loop to exist at import time (Python 3.12+)
if not asyncio._get_running_loop():
    asyncio.set_event_loop(asyncio.new_event_loop())

from classes.auth import Authenticator
from classes.exceptions import BotError
from classes.runner import BotRunner
from config import Config

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Telegram Referral Bot — automate referral invitations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python bot.py --auth -t accounts.txt              Authenticate accounts
  python bot.py --run -t accounts.txt               Run referral bot
  python bot.py --run -t accounts.txt --channel     Run with channel join
  python bot.py --run -t accounts.txt -p proxies.txt  Run with proxies
  python bot.py --run -t accounts.txt --strings     Run with string sessions
  python bot.py --interactive                        Interactive mode
""",
    )

    parser.add_argument(
        "-a", "--auth", action="store_true",
        help="Authenticate accounts and create session files",
    )
    parser.add_argument(
        "-r", "--run", action="store_true",
        help="Run the referral bot",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true",
        help="Start in interactive mode (prompts for all settings)",
    )
    parser.add_argument(
        "-t", "--tokens", type=str, metavar="FILE",
        help="Path to the tokens/accounts file",
    )
    parser.add_argument(
        "-p", "--proxies", type=str, metavar="FILE",
        help="Path to the proxies file",
    )
    parser.add_argument(
        "-ch", "--channel", action="store_true",
        help="Enable joining a channel before sending /start",
    )
    parser.add_argument(
        "-s", "--strings", action="store_true",
        help="Use pyrogram string sessions instead of session files",
    )

    return parser


def run_interactive() -> None:
    config = Config.interactive()
    config.validate_files()

    action = input("\nAction — (a)uth or (r)un: ").strip().lower()

    if action in ("a", "auth"):
        _do_auth(config)
    elif action in ("r", "run"):
        _do_run(config)
    else:
        logger.error("Unknown action: %s", action)
        sys.exit(1)


def run_cli(args: argparse.Namespace) -> None:
    if not args.tokens:
        logger.error("Tokens file is required. Use -t / --tokens FILE")
        sys.exit(1)

    config = Config.from_env(
        tokens_file=Path(args.tokens),
        proxies_file=Path(args.proxies) if args.proxies else None,
        join_channel=args.channel or None,
        use_string_sessions=args.strings or None,
    )
    config.validate_files()

    if args.auth:
        _do_auth(config)
    if args.run:
        _do_run(config)


def _do_auth(config: Config) -> None:
    authenticator = Authenticator(
        tokens_file=config.tokens_file,
        proxies_file=config.proxies_file,
        sessions_dir=config.sessions_dir,
    )
    authenticator.run()


def _do_run(config: Config) -> None:
    runner = BotRunner(config)
    if not config.use_string_sessions:
        runner.ensure_sessions_dir()
    runner.run()


def main() -> None:
    setup_logging()
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.interactive:
            run_interactive()
        elif args.auth or args.run:
            run_cli(args)
        else:
            parser.print_help()
            sys.exit(1)
    except BotError as e:
        logger.error("%s", e)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(130)

    logger.info("Done")


if __name__ == "__main__":
    main()

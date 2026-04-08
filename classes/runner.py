from __future__ import annotations

import logging
import random
import time
from pathlib import Path

from pyrogram.raw import functions

from classes.client_factory import create_client
from classes.models import Proxy, Token
from config import Config

logger = logging.getLogger(__name__)


class BotRunner:
    """Runs the referral bot: connects accounts and sends /start with referral param."""

    def __init__(self, config: Config) -> None:
        self._config = config

    def ensure_sessions_dir(self) -> None:
        self._config.sessions_dir.mkdir(exist_ok=True)

    def run(self) -> None:
        tokens = Token.load_from_file(self._config.tokens_file)
        proxies = self._load_proxies()

        if len(tokens) < self._config.count:
            logger.error(
                "Not enough tokens: found %d, need %d",
                len(tokens),
                self._config.count,
            )
            return

        success_count = 0

        for i in range(self._config.count):
            token = tokens[i]
            proxy = proxies[i] if i < len(proxies) else None
            label = self._get_label(token, i)

            try:
                client = create_client(token, proxy, self._config.sessions_dir)
                client.connect()

                try:
                    if self._config.join_channel and self._config.channel_name:
                        if self._join_channel(client):
                            logger.info("[%s] Joined channel @%s", label, self._config.channel_name)
                        else:
                            logger.warning("[%s] Failed to join channel @%s", label, self._config.channel_name)

                    if self._start_bot(client):
                        logger.info("[%s] Sent /start to @%s", label, self._config.bot_name)
                        success_count += 1
                    else:
                        logger.warning("[%s] Failed to send /start", label)
                finally:
                    client.disconnect()

                if i < self._config.count - 1:
                    delay = random.randint(self._config.delay_min, self._config.delay_max)
                    logger.info("Waiting %d seconds...", delay)
                    time.sleep(delay)

            except Exception:
                logger.exception("[%s] Error processing account", label)

        logger.info("Completed: %d/%d successful", success_count, self._config.count)

    def _load_proxies(self) -> list[Proxy | None]:
        if self._config.proxies_file and self._config.proxies_file.exists():
            return Proxy.load_from_file(self._config.proxies_file)
        return []

    def _join_channel(self, client) -> bool:
        try:
            target = client.resolve_peer(self._config.channel_name)
            result = client.invoke(functions.channels.JoinChannel(channel=target))
            return result.chats[0].username == self._config.channel_name
        except Exception:
            logger.exception("Failed to join channel")
            return False

    def _start_bot(self, client) -> bool:
        try:
            target = client.resolve_peer(self._config.bot_name)
            client.invoke(
                functions.messages.StartBot(
                    bot=target,
                    peer=target,
                    random_id=random.randint(100000, 999999),
                    start_param=self._config.refer_id,
                )
            )
            return True
        except Exception:
            logger.exception("Failed to start bot")
            return False

    @staticmethod
    def _get_label(token: Token, index: int) -> str:
        if token.is_string_session:
            return f"Session {index + 1}"
        return token.session_name

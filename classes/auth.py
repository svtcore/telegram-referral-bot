from __future__ import annotations

import logging
from pathlib import Path

from classes.client_factory import create_client
from classes.models import Proxy, Token

logger = logging.getLogger(__name__)


class Authenticator:
    """Creates Pyrogram session files by authenticating each account"""

    def __init__(
        self,
        tokens_file: Path,
        proxies_file: Path | None = None,
        sessions_dir: Path = Path("sessions"),
    ) -> None:
        self._tokens_file = tokens_file
        self._proxies_file = proxies_file
        self._sessions_dir = sessions_dir

    def run(self) -> None:
        tokens = Token.load_from_file(self._tokens_file)
        proxies = self._load_proxies()

        for i, token in enumerate(tokens):
            if token.is_string_session:
                logger.info("Skipping string session #%d (no auth needed)", i + 1)
                continue

            proxy = proxies[i] if i < len(proxies) else None
            label = token.session_name

            try:
                client = create_client(token, proxy, self._sessions_dir)
                client.start()
                client.stop()
                logger.info("[%s] Session created successfully", label)
            except Exception:
                logger.exception("[%s] Authentication failed", label)

        logger.info("Authentication complete")

    def _load_proxies(self) -> list[Proxy | None]:
        if self._proxies_file and self._proxies_file.exists():
            return Proxy.load_from_file(self._proxies_file)
        return []

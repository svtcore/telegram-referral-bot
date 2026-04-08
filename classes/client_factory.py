from __future__ import annotations

import hashlib
from pathlib import Path

from pyrogram import Client

from classes.models import Proxy, Token


def create_client(
    token: Token,
    proxy: Proxy | None = None,
    sessions_dir: Path = Path("sessions"),
) -> Client:
    """Create a Pyrogram Client from a Token and optional Proxy.

    Eliminates duplicated connect logic where single source of truth for client creation.
    """
    proxy_dict = proxy.to_pyrogram_dict() if proxy else None

    if token.is_string_session:
        session_hash = hashlib.md5(token.session_name.encode()).hexdigest()
        return Client(
            name=str(sessions_dir / session_hash),
            session_string=token.session_name,
            proxy=proxy_dict,
        )

    return Client(
        name=str(sessions_dir / token.session_name),
        api_id=token.api_id,
        api_hash=token.api_hash,
        proxy=proxy_dict,
    )

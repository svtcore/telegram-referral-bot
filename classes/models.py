from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from classes.exceptions import ProxyError, TokenError


@dataclass(frozen=True)
class Token:
    session_name: str
    api_id: int | None = None
    api_hash: str | None = None
    is_string_session: bool = False

    @classmethod
    def parse(cls, line: str) -> Token:
        line = line.strip()
        if not line:
            raise TokenError("Empty token line")

        parts = line.split(":")
        if len(parts) == 3:
            try:
                api_id = int(parts[1])
            except ValueError as e:
                raise TokenError(f"Invalid API_ID '{parts[1]}': must be an integer") from e
            return cls(
                session_name=parts[0],
                api_id=api_id,
                api_hash=parts[2],
            )
        if len(parts) == 1:
            return cls(session_name=line, is_string_session=True)

        raise TokenError(f"Invalid token format (expected NAME:API_ID:API_HASH or STRING_SESSION): {line[:40]}...")

    @classmethod
    def load_from_file(cls, path: Path) -> list[Token]:
        try:
            with open(path, encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
        except FileNotFoundError as e:
            raise TokenError(f"Tokens file not found: {path}") from e

        if not lines:
            raise TokenError(f"Tokens file is empty: {path}")

        return [cls.parse(line) for line in lines]


@dataclass(frozen=True)
class Proxy:
    hostname: str
    port: int
    username: str | None = None
    password: str | None = None
    scheme: str = "socks5"

    @classmethod
    def parse(cls, line: str) -> Proxy | None:
        line = line.strip()
        if not line:
            return None

        parts = line.split(":")
        if len(parts) == 4:
            try:
                port = int(parts[1])
            except ValueError as e:
                raise ProxyError(f"Invalid proxy port '{parts[1]}'") from e
            return cls(
                hostname=parts[0],
                port=port,
                username=parts[2],
                password=parts[3],
            )
        if len(parts) == 2:
            try:
                port = int(parts[1])
            except ValueError as e:
                raise ProxyError(f"Invalid proxy port '{parts[1]}'") from e
            return cls(hostname=parts[0], port=port)

        raise ProxyError(f"Invalid proxy format (expected IP:PORT or IP:PORT:LOGIN:PASSWORD): {line}")

    @classmethod
    def load_from_file(cls, path: Path) -> list[Proxy | None]:
        try:
            with open(path, encoding="utf-8") as f:
                lines = [line.strip() for line in f]
        except FileNotFoundError as e:
            raise ProxyError(f"Proxies file not found: {path}") from e

        return [cls.parse(line) for line in lines]

    def to_pyrogram_dict(self) -> dict:
        proxy = {
            "hostname": self.hostname,
            "port": self.port,
            "scheme": self.scheme,
        }
        if self.username and self.password:
            proxy["username"] = self.username
            proxy["password"] = self.password
        return proxy

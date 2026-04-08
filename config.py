from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

from classes.exceptions import ConfigError


@dataclass(frozen=True)
class Config:
    bot_name: str
    count: int
    refer_id: str
    delay_min: int = 10
    delay_max: int = 15
    channel_name: str | None = None
    join_channel: bool = False
    tokens_file: Path = field(default_factory=lambda: Path("accounts.txt"))
    proxies_file: Path | None = None
    use_string_sessions: bool = False
    sessions_dir: Path = field(default_factory=lambda: Path.cwd() / "sessions")

    def __post_init__(self) -> None:
        if not self.bot_name:
            raise ConfigError("BOT_NAME is required")
        if self.count < 1:
            raise ConfigError("COUNT must be at least 1")
        if not self.refer_id:
            raise ConfigError("REFER_ID is required")
        if self.delay_min < 0 or self.delay_max < 0:
            raise ConfigError("Delay values must be non-negative")
        if self.delay_min > self.delay_max:
            raise ConfigError("DELAY_MIN must be less than or equal to DELAY_MAX")

    @classmethod
    def from_env(cls, env_path: str = ".env", **overrides: object) -> Config:
        load_dotenv(env_path)

        try:
            kwargs: dict = {
                "bot_name": os.getenv("BOT_NAME", "").strip(),
                "count": int(os.getenv("COUNT", "0").strip()),
                "refer_id": os.getenv("REFER_ID", "").strip(),
                "delay_min": int(os.getenv("DELAY_MIN", "10").strip()),
                "delay_max": int(os.getenv("DELAY_MAX", "15").strip()),
                "channel_name": os.getenv("CHANNEL_NAME", "").strip() or None,
            }
        except ValueError as e:
            raise ConfigError(f"Invalid value in .env: {e}") from e

        kwargs.update({k: v for k, v in overrides.items() if v is not None})
        return cls(**kwargs)

    @classmethod
    def interactive(cls) -> Config:
        print("\n--- Interactive Configuration ---\n")

        bot_name = _prompt("Bot name (without @)")
        count = int(_prompt("Number of accounts to use"))
        refer_id = _prompt("Referral ID")
        delay_min = int(_prompt("Minimum delay in seconds", "10"))
        delay_max = int(_prompt("Maximum delay in seconds", "15"))
        channel_name = _prompt("Channel name (leave empty to skip)", "") or None
        join_channel = channel_name is not None and _confirm("Join channel before /start?")
        tokens_file = Path(_prompt("Tokens file path", "accounts.txt"))
        proxies_str = _prompt("Proxies file path (leave empty for none)", "")
        proxies_file = Path(proxies_str) if proxies_str else None
        use_strings = _confirm("Use pyrogram string sessions?")

        return cls(
            bot_name=bot_name,
            count=count,
            refer_id=refer_id,
            delay_min=delay_min,
            delay_max=delay_max,
            channel_name=channel_name,
            join_channel=join_channel,
            tokens_file=tokens_file,
            proxies_file=proxies_file,
            use_string_sessions=use_strings,
        )

    def validate_files(self) -> None:
        if not self.tokens_file.exists():
            raise ConfigError(f"Tokens file not found: {self.tokens_file}")
        if self.proxies_file and not self.proxies_file.exists():
            raise ConfigError(f"Proxies file not found: {self.proxies_file}")


def _prompt(message: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{message}{suffix}: ").strip()
    return value or default


def _confirm(message: str, default: bool = False) -> bool:
    hint = " (y/N)" if not default else " (Y/n)"
    answer = input(f"{message}{hint}: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")

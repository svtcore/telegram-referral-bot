class BotError(Exception):
    """Base exception for the telegram referral bot."""


class ConfigError(BotError):
    """Raised when configuration is invalid or missing."""


class TokenError(BotError):
    """Raised when token parsing or loading fails."""


class ProxyError(BotError):
    """Raised when proxy parsing or loading fails."""

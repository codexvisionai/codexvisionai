import os
from dataclasses import dataclass

@dataclass
class Config:
    bot_token: str
    provider_token: str
    admin_id: int | None = None


def load_config() -> Config:
    return Config(
        bot_token=os.getenv("BOT_TOKEN", ""),
        provider_token=os.getenv("PROVIDER_TOKEN", ""),
        admin_id=int(os.getenv("ADMIN_ID", "0")) or None,
    )

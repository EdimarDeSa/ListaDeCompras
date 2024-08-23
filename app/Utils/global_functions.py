import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Optional


def datetime_now_utc() -> datetime:
    return datetime.now(UTC)


class MsgLoader:
    __messages: Optional[dict] = None

    @classmethod
    def _load_messages(cls):
        if cls.__messages is None:
            with open(Path(__file__).resolve().parent.parent.parent / "./messages.json", "r") as file:
                cls.__messages = json.load(file)

    @classmethod
    def get_message(cls, message_name: str, language: str = "Pt_Br") -> str:
        cls._load_messages()
        return cls.__messages[language][message_name]

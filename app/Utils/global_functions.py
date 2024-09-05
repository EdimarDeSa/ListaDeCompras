import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Optional

from app.Enums.enums import ResponseCode, LangEnum


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
    def get_message(cls, rc: ResponseCode, language: str = LangEnum.EN_US) -> str:
        cls._load_messages()
        language_dict = cls.__messages.get(language, {})
        message = language_dict.get(rc.name, rc.name)
        return message

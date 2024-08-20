from datetime import UTC, datetime


def datetime_now_utc() -> datetime:
    return datetime.now(UTC)

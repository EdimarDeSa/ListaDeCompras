from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from Enums.enums import LangEnum
from Utils.global_functions import get_expire_time


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID
    email: str = Field(examples=["your.email@domain.com"])
    is_active: bool
    language: LangEnum
    expires_at: Optional[int] = Field(
        default_factory=get_expire_time, serialization_alias="exp", validation_alias="exp", init=True
    )

    def expire_date(self) -> datetime:
        return datetime.fromtimestamp(self.expires_at)

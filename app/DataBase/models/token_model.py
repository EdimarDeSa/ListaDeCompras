from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.Enums.enums import LangEnum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID
    email: str = Field(examples=["your.email@domain.com"])
    is_active: bool = True
    language: LangEnum = LangEnum.EN_US
    expires_at: Optional[int] = Field(default=None, alias="exp")

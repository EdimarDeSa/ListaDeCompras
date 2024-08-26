from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.Utils.global_functions import datetime_now_utc


class BaseRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[UUID] = None
    name: str
    creation: Optional[datetime] = Field(default_factory=datetime_now_utc, frozen=True)
    last_update: Optional[datetime] = Field(default_factory=datetime_now_utc, frozen=True)

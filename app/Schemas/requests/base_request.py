from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict

from Utils.global_functions import datetime_now_utc


class BaseRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4, frozen=True, exclude=True)
    name: str
    creation: datetime = Field(default_factory=datetime_now_utc, frozen=True, exclude=True, init=False)
    last_update: datetime = Field(default_factory=datetime_now_utc, frozen=True, init=False)

    def __str__(self) -> str:
        return f"<Name: {self.name}>"

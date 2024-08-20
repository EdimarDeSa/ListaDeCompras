import re
import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator
from typing_extensions import Self

from app.Enums.enums import LangEnum, MessagesEnum
from app.Utils.types import ErrorsDict
from app.Utils.utils import datetime_now_utc


class BaseDTO(BaseModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, frozen=True)
    name: str = Field(max_length=100)
    creation: datetime = Field(default_factory=datetime_now_utc, frozen=True)
    last_update: datetime = Field(
        default_factory=datetime_now_utc,
        frozen=True,
    )


class UserDTO(BaseDTO):
    email: EmailStr = Field(
        examples=[
            "your.email@domain.com",
        ]
    )
    language: LangEnum = Field(default=LangEnum.PT_BR)
    birthdate: date


class NewUser(BaseDTO):
    name: str = Field(max_length=100)
    email: EmailStr = Field(
        examples=[
            "your.email@domain.com",
        ]
    )
    language: LangEnum = Field(default=LangEnum.PT_BR)
    password: str = Field(max_length=255, examples=["P@s5W0rD"])
    birthdate: date

    @model_validator(mode="after")
    def validate_password(self) -> Self:

        errors: ErrorsDict = ErrorsDict()

        if not self.password:
            errors.insert(MessagesEnum.PASSWORD_NULL, self.language)
            raise ValueError(errors)

        if len(self.password) < 8:
            errors.insert(MessagesEnum.PASSWORD_LENGHT, self.language)

        if not re.search(r"\d", self.password):
            errors.insert(MessagesEnum.PASSWORD_NEED_NUMBER, self.language)

        if not re.search(r"[A-Z]", self.password):
            errors.insert(MessagesEnum.PASSWORD_NEED_UPPER_CASE, self.language)

        if not re.search(r"[a-z]", self.password):
            errors.insert(MessagesEnum.PASSWORD_NEED_LOWER_CASE, self.language)

        if not re.search(r"[\W_]", self.password):
            errors.insert(MessagesEnum.PASSWORD_NEED_SPECIAL, self.language)

        if errors:
            raise ValueError(errors)

        return self


class DefaultCategoryDTO(BaseDTO):
    pass


class UnityTypeDTO(BaseDTO):
    base_calc: int = 1


class DefaultProductDTO(BaseDTO):
    unit_type_id: uuid.UUID
    category_id: uuid.UUID
    image_url: str

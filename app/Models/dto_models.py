import re
import uuid
from datetime import date

from pydantic import EmailStr, Field, model_validator
from typing_extensions import Self

from app.Enums.enums import LangEnum, MessagesEnum
from app.Schemas.requests.base_request import BaseRequest
from app.Utils.types import ErrorsDict


class BaseUserPropertyDTO(BaseRequest):
    name: str = Field(max_length=255)
    user_id: uuid.UUID


class UserDTO(BaseRequest):
    email: EmailStr = Field(
        examples=[
            "your.email@domain.com",
        ]
    )
    language: LangEnum = Field(default=LangEnum.PT_BR)
    birthdate: date


class NewUser(UserDTO):
    password: str = Field(max_length=255, examples=["P@s5W0rD"])

    @model_validator(mode="after")
    def validate_password(self) -> Self:

        errors: ErrorsDict = ErrorsDict()

        if not self.password:
            errors.insert(MessagesEnum.PASSWORD_NULL, self.language)
            raise ValueError(errors)

        if len(self.password) < 8:
            errors.insert(MessagesEnum.PASSWORD_LENGTH, self.language)

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


class DefaultCategoryDTO(BaseRequest):
    pass


class UnityTypeDTO(BaseRequest):
    base_calc: int = 1


class DefaultProductDTO(BaseRequest):
    unit_type_id: uuid.UUID
    category_id: uuid.UUID
    image_url: str


class MarketDTO(BaseUserPropertyDTO):
    pass


class UserCategorysDTO(BaseUserPropertyDTO):
    pass


class UserProductsDTO(BaseUserPropertyDTO):
    unity_types_id: uuid.UUID
    price: float
    price_unity_types_id: uuid.UUID
    category_id: uuid.UUID
    notes: str
    barcode: str
    image_url: str


class ShoppingListDTO(BaseUserPropertyDTO):
    final_value: float
    unique_items: int
    total_items: int


class ShoppingLogDTO(BaseUserPropertyDTO):
    shopping_list_id: uuid.UUID
    market_id: uuid.UUID
    buy_date: date


class ProductListDTO(BaseRequest):
    shopping_list_id: uuid.UUID
    user_product_id: uuid.UUID
    quantity: int
    price: float
    total: float = 0
    on_cart: bool = False

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import Field, BaseModel

from app.Enums.enums import LangEnum
from app.Schemas.requests.base_request import BaseRequest
from app.Utils.global_functions import datetime_now_utc


class BaseUserPropertyDTO(BaseRequest):
    user_id: uuid.UUID


class UserDTO(BaseRequest):
    email: str = Field(examples=["your.email@domain.com"])
    language: LangEnum = LangEnum.EN
    birthdate: date

    def __eq__(self, other) -> bool:
        return all(
            [
                self.id == other.id,
                self.name == other.name,
                self.email == other.email,
                self.birthdate == other.birthdate,
            ]
        )


class UpdateUserDTO(BaseModel):
    id: uuid.UUID
    name: Optional[str] = None
    email: Optional[str] = Field(default=None, examples=["your.email@domain.com"])
    language: Optional[LangEnum] = None
    birthdate: Optional[date] = None
    last_update: Optional[datetime] = Field(default_factory=datetime_now_utc, frozen=True)


class NewUser(UserDTO):
    password: str = Field(examples=["P@s5W0rD"])


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

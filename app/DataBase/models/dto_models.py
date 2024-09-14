import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import Field, BaseModel, ConfigDict

from Enums.enums import LangEnum
from Schemas.requests.base_request import BaseRequest
from Utils.global_functions import datetime_now_utc


class BaseUserPropertyDTO(BaseRequest):
    user_id: uuid.UUID

    def __repr__(self) -> str:
        return f"<Id: {self.user_id}> | <Name: {self.name}>"


class UserDTO(BaseRequest):
    email: str = Field(examples=["your.email@domain.com"])
    language: LangEnum = LangEnum.EN_US
    birthdate: date

    def __repr__(self) -> str:
        return f"<Id: {self.user_id}> | <Name: {self.name}>"


class UserLoginDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    password: str
    email: str = Field(examples=["your.email@domain.com"])
    language: LangEnum = LangEnum.EN_US
    is_active: bool


class UpdateUserDTO(BaseModel):
    name: Optional[str] = None
    language: Optional[LangEnum] = None
    birthdate: Optional[date] = None
    last_update: Optional[datetime] = Field(default_factory=datetime_now_utc, exclude=True)


class UpdateUserEmailDTO(BaseModel):
    email: str = Field(default=None, examples=["your.email@domain.com"])
    last_update: datetime = Field(default_factory=datetime_now_utc, exclude=True)


class UpdateUserPasswordDTO(BaseModel):
    password: str = Field(examples=["P@s5W0rD"])
    last_update: datetime = Field(default_factory=datetime_now_utc, exclude=True)


class NewUser(BaseRequest):
    password: str = Field(examples=["P@s5W0rD"])
    email: str = Field(examples=["your.email@domain.com"])
    language: LangEnum = LangEnum.PT_BR
    birthdate: date


class DefaultCategoryDTO(BaseRequest):
    pass


class UnityTypeDTO(BaseRequest):
    base_calc: int = 1


class MarketDTO(BaseUserPropertyDTO):
    pass


class UserCategoryDTO(BaseUserPropertyDTO):
    pass


class NewUserCategory(BaseUserPropertyDTO):
    pass


class UserProductDTO(BaseUserPropertyDTO):
    unity_types_id: uuid.UUID
    price: float = 0.0
    price_unity_types_id: uuid.UUID
    category_id: uuid.UUID
    notes: Optional[str] = None
    barcode: Optional[str] = None
    image_url: Optional[str] = None


class NewUserProduct(UserProductDTO):
    pass


class ShoppingListDTO(BaseUserPropertyDTO):
    final_value: float
    unique_items: int = 0
    total_items: int = 0


class ShoppingLogDTO(BaseUserPropertyDTO):
    shopping_list_id: uuid.UUID
    market_id: uuid.UUID
    buy_date: date = Field(default_factory=date.today)


class ProductListDTO(BaseRequest):
    shopping_list_id: uuid.UUID
    user_product_id: uuid.UUID
    quantity: int = 0
    price: float = 0.0
    total: float = 0.0
    on_cart: bool = False

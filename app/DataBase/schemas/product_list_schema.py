from sqlalchemy import Integer, ForeignKey, Boolean
from sqlalchemy.orm import MappedColumn

from DataBase.schemas.base_schemas import BaseSchema


class ProductList(BaseSchema):
    __tablename__ = "product_list"

    shopping_list_id = MappedColumn(Integer, ForeignKey("shopping_list.id"), nullable=False)
    user_product_id = MappedColumn(Integer, ForeignKey("user_products.id"), nullable=False)
    quantity = MappedColumn(Integer, default=1)
    price = MappedColumn(Integer, default=0)
    total = MappedColumn(Integer, default=0)
    on_cart = MappedColumn(Boolean, default=False)

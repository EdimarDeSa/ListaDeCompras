import uuid

from Schemas.requests.base_request import BaseRequest


class DefaultProductDTO(BaseRequest):
    unit_type_id: uuid.UUID
    default_category_id: uuid.UUID
    image_url: str = ""


class NewDefaultProduct(BaseRequest):
    unit_type_name: str
    default_category_name: str
    image_url: str = ""

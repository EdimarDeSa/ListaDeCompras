from app.Schemas.requests.base_request import BaseRequest


class DefaultProductDTO(BaseRequest):
    unit_type_name: str
    default_category_name: str
    image_url: str = ""


class NewDefaultProduct(DefaultProductDTO):
    pass

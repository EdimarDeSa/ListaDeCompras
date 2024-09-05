from typing import Optional, Mapping, Any

from fastapi import Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.background import BackgroundTask


class BaseContent(BaseModel):
    rc: int = 0
    data: Any = None


class BaseResponse(Response):
    def __init__(
        self,
        *,
        status_code: int = 200,
        content: BaseContent,
        headers: Optional[Mapping[str, str]] = None,
        media_type: Optional[str] = "application/json",
        background: Optional[BackgroundTask] = None
    ):
        json_content = jsonable_encoder(content.model_dump_json())

        super().__init__(
            content=json_content, status_code=status_code, headers=headers, media_type=media_type, background=background
        )

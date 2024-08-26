from pydantic import BaseModel


class VersionModel(BaseModel):
    version: str

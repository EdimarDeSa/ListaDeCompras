from pydantic import BaseModel


class VersionModel(BaseModel):
    major: str
    minor: str
    patch: str

    @classmethod
    def from_string(cls, version_string: str) -> "VersionModel":
        major, minor, patch = version_string.split(".")
        return cls(major=major, minor=minor, patch=patch)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

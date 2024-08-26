from logging import Logger

from app.Repositories.base_repository import BaseRepository
from app.Services.base_service import BaseService
from app.Validators.base_validator import BaseValidator


class UtilsService(BaseService):
    def check_health(self):
        pass

    def get_version(self):
        pass

    def _create_repository(self) -> type[BaseRepository]:
        pass

    def _create_validator(self) -> type[BaseValidator]:
        pass

    def _create_logger(self) -> Logger:
        return Logger(__name__)

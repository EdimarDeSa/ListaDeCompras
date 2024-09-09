from uuid import UUID

from sqlalchemy.orm import Session, scoped_session

from app.DataBase.models.dto_models import DefaultCategoryDTO
from app.Enums.enums import LangEnum
from app.Repositories.base_repository import BaseRepository


class UserProductsRepository(BaseRepository):
    def __init__(self):
        self._query = self.create_query()
        self._logger = self.create_logger(__name__)

    def create_default_user_categories(
        self,
        db_session: scoped_session[Session],
        id_user: UUID,
        default_categories: list[DefaultCategoryDTO],
        language: LangEnum,
    ) -> None:

        pass

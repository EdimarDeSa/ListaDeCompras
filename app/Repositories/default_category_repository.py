from sqlalchemy import Sequence
from sqlalchemy.orm import scoped_session, Session

from app.DataBase.models.dto_models import DefaultCategoryDTO
from app.DataBase.schemas.default_category_schema import DefaultCategory
from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.internal_errors import InternalErrors
from app.Repositories.base_repository import BaseRepository


class DefaultCategoryRepository(BaseRepository):
    def __init__(self):
        self._query = self.create_query()
        self._logger = self.create_logger(__name__)

    def read_all(self, db_session: scoped_session[Session], language: LangEnum) -> list[DefaultCategoryDTO]:

        try:
            query = self._query.select_all_default_categories()

            result: Sequence[DefaultCategory] = db_session.execute(query).scalars().all()

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.CATEGORY_NOT_FOUND, language=language)

            categories = [DefaultCategoryDTO.model_validate(c) for c in result]

            return categories

        except Exception as e:
            self.return_db_error(e, language)

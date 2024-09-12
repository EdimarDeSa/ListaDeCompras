from sqlalchemy.orm import scoped_session, Session

from DataBase.models.dto_models import DefaultCategoryDTO
from DataBase.schemas.default_category_schema import DefaultCategory
from Enums.enums import LangEnum, ResponseCode
from InternalResponse.internal_errors import InternalErrors
from Repositories.base_repository import BaseRepository


class DefaultCategoryRepository(BaseRepository):
    def __init__(self):
        self._query = self.create_query()
        self._logger = self.create_logger(__name__)

    def select_all(self, db_session: scoped_session[Session], language: LangEnum) -> list[DefaultCategoryDTO]:
        self._logger.info(f"Starting select_all")
        try:
            query = self._query.select_all_default_categories()

            self._logger.debug("Searching all default categories")
            result: list[DefaultCategory] = list(db_session.execute(query).scalars().all())
            self._logger.info(f"Default categories found: {len(result)}")

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.CATEGORY_NOT_FOUND, language=language)

            categories = [DefaultCategoryDTO.model_validate(c, from_attributes=True) for c in result]

            return categories

        except Exception as e:
            self.return_db_error(e, language)

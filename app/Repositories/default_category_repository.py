from sqlalchemy.orm import scoped_session, Session

from app.DataBase.models.dto_models import DefaultCategoryDTO
from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.internal_errors import InternalErrors
from app.Repositories.base_repository import BaseRepository


class DefaultCategoryRepository(BaseRepository):
    def read_all(self, db_session: scoped_session[Session], language: LangEnum) -> list[DefaultCategoryDTO]:
        self.db_session = db_session

        try:
            query = self.query.select_all_default_categories()

            result = self.db_session.execute(query).all()

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.CATEGORY_NOT_FOUND, language=language)

            categories = [DefaultCategoryDTO.model_validate(c.DefaultCategory) for c in result]

            return categories

        except Exception as e:
            self.return_db_error(e, language)

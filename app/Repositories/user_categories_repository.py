from sqlalchemy.orm import Session, scoped_session

from app.DataBase.models.dto_models import NewCategory
from app.Enums.enums import LangEnum
from app.Repositories.base_repository import BaseRepository


class UserCategoriesRepository(BaseRepository):
    def __init__(self):
        self._query = self.create_query()
        self._logger = self.create_logger(__name__)

    def create_default_user_categories(
        self,
        db_session: scoped_session[Session],
        new_categories: list[NewCategory],
        language: LangEnum,
    ) -> None:
        self._logger.info("Starting create_default_user_categories")

        try:
            self._logger.debug("Creating user categories data")
            categories_data = [c.model_dump(exclude_none=True) for c in new_categories]

            query = self._query.insert_user_categories(categories_data)

            db_session.execute(query)
            db_session.flush()

            self._logger.info("User categories created successfully")

        except Exception as e:
            self.return_db_error(e, language)

import uuid

from sqlalchemy import Sequence
from sqlalchemy.orm import Session, scoped_session

from DataBase.models.dto_models import NewUserCategory, UserCategoryDTO
from DataBase.schemas.user_categories_schema import UserCategories
from Enums.enums import LangEnum
from Repositories.base_repository import BaseRepository


class UserCategoriesRepository(BaseRepository):
    def __init__(self):
        self._query = self.create_query()
        self._logger = self.create_logger(__name__)

    def create_default_user_categories(
        self,
        db_session: scoped_session[Session],
        new_categories: list[NewUserCategory],
        language: LangEnum,
    ) -> None:
        self._logger.info("Starting create_default_user_categories")

        try:

            self._logger.debug("Creating user categories data")
            categories_data = [c.model_dump(exclude_none=True) for c in new_categories]

            self._logger.debug(f"Inserting user categories on table {UserCategories.__tablename__}")
            query = self._query.insert_user_categories(categories_data)

            db_session.execute(query)
            db_session.flush()

            self._logger.info("User categories created successfully")

        except Exception as e:
            self.return_db_error(e, language)

    def get_all_user_categories_by_user_id(
        self, db_session: scoped_session[Session], user_id: uuid.UUID, language: LangEnum
    ) -> list[UserCategoryDTO]:
        self._logger.info("Starting get_all_user_categories")

        try:
            self._logger.debug(f"Selecting user categories on table {UserCategories.__tablename__}")
            query = self._query.select_all_user_categories(user_id)

            self._logger.debug("Getting all user categories")
            categories: Sequence[UserCategories] = db_session.execute(query).all()

            self._logger.info("User categories retrieved successfully")

            return [UserCategoryDTO.model_validate(cat) for cat in categories]

        except Exception as e:
            self.return_db_error(e, language)

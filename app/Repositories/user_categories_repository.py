import uuid

from sqlalchemy import Sequence
from sqlalchemy.orm import Session, scoped_session

from DataBase.models.dto_models import NewUserCategory, UserCategoryDTO
from DataBase.schemas.default_category_schema import DefaultCategory
from DataBase.schemas.user_categories_schema import UserCategory
from Enums.enums import LangEnum
from Repositories.base_repository import BaseRepository


class UserCategoriesRepository(BaseRepository):
    def __init__(self):
        self._query = self.create_query()
        self._logger = self.create_logger(__name__)

    def get_all_user_categories_by_user_id(
        self, db_session: scoped_session[Session], user_id: uuid.UUID, language: LangEnum
    ) -> list[UserCategoryDTO]:
        self._logger.info("Starting get_all_user_categories")

        try:
            self._logger.debug(f"Selecting user categories on table {UserCategory.__tablename__}")
            query = self._query.select_all_user_categories(user_id)

            self._logger.debug("Getting all user categories")
            categories: Sequence[UserCategory] = db_session.execute(query).all()

            self._logger.info("User categories retrieved successfully")

            return [UserCategoryDTO.model_validate(cat, from_attributes=True) for cat in categories]

        except Exception as e:
            self.return_db_error(e, language)

    def create_default_user_categories(
        self,
        db_session: scoped_session[Session],
        user_id: uuid.UUID,
        language: LangEnum,
    ) -> None:
        self._logger.info("Starting create_default_user_categories")

        try:
            self._logger.debug("Selecting all default categories")
            query = self._query.select_all_default_categories_names()
            default_categories: list[DefaultCategory.name] = list(db_session.execute(query).scalars().all())

            for category in default_categories:
                self._logger.debug(f"Creating user category - '{category}'")
                new_category = NewUserCategory(user_id=user_id, name=category)
                self.create_user_category(db_session, new_category, language)

        except Exception as e:
            self.return_db_error(e, language)

    def create_user_category(
        self, db_session: scoped_session[Session], new_user_category: NewUserCategory, language: LangEnum
    ) -> UserCategoryDTO:
        try:
            self._logger.debug(f"Inserting user category on table {UserCategory.__tablename__}")
            user_cat_data = new_user_category.model_dump(exclude_none=True)

            self._logger.debug(f"Inserting user category {new_user_category.name} for user {new_user_category.user_id}")
            query = self._query.insert_user_category(user_cat_data)

            result = db_session.execute(query)
            db_session.flush()

            self._logger.info("User categories created successfully")

            return UserCategoryDTO.model_validate(result.last_inserted_params(), from_attributes=True)

        except Exception as e:
            self.return_db_error(e, language)

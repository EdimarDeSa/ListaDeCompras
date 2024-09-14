from uuid import UUID

from sqlalchemy.orm import Session, scoped_session

from DataBase.models.dto_models import NewUserProduct, UserProductDTO
from DataBase.schemas.default_product_schema import DefaultProduct
from DataBase.schemas.user_categories_schema import UserCategory
from DataBase.schemas.user_products_schema import UserProduct
from Enums.enums import LangEnum
from Repositories.base_repository import BaseRepository


class UserProductsRepository(BaseRepository):
    def __init__(self):
        self._query = self.create_query()
        self._logger = self.create_logger(__name__)

    def create_default_user_products(
        self,
        db_session: scoped_session[Session],
        user_id: UUID,
        language: LangEnum,
    ) -> None:
        self._logger.info("Starting create_default_user_products")

        try:
            self._logger.debug("Selecting all default products")
            def_prod_query = self._query.select_all_default_products()
            default_products: list[DefaultProduct] = list(db_session.execute(def_prod_query).scalars().all())
            self._logger.debug("Default products selected")

            self._logger.debug(f"Creating products for User: {user_id}")
            for product in default_products:
                self._logger.debug(f"Creating product: {product.name}")

                self._logger.debug(
                    f"Searching category by <Name: {product.default_category.name}> and <User.id" f": {user_id}>"
                )
                query = self._query.select_user_category_id_by_name(user_id, product.default_category.name)
                category_id: UserCategory.id = db_session.execute(query).scalar()
                self._logger.debug(f"Category id: {category_id}")

                new_product = NewUserProduct(
                    user_id=user_id,
                    unity_types_id=product.unit_type_id,
                    price_unity_types_id=product.unit_type_id,
                    category_id=category_id,
                    name=product.name,
                    image_url=product.image_url,
                )
                self.create_user_product(db_session, new_product, language)

            db_session.flush()

        except Exception as e:
            self.return_db_error(e, language)

    def create_user_product(
        self, db_session: scoped_session[Session], new_product: NewUserProduct, language: LangEnum
    ) -> UserProductDTO:
        self._logger.info("Starting create_user_product")

        try:
            self._logger.debug(f"Inserting user product on table: {UserProduct.__tablename__}")
            new_product_data = new_product.model_dump(exclude_none=True)

            query = self._query.insert_user_product(new_product_data)

            result = db_session.execute(query)
            db_session.flush()

            self._logger.info("User product created successfully")

            return UserProductDTO.model_validate(result.last_inserted_params(), from_attributes=True)

        except Exception as e:
            self.return_db_error(e, language)

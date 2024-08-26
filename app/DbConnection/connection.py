from os import getenv
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session


def get_db_url() -> str:
    db_dialect: str = getenv("DB_DIALECT", "postgresql")
    db_user: str = getenv("DB_USER", "postgres")
    db_password: str = getenv("DB_PASSWORD", "postgres")
    db_ip: str = getenv("DB_IP", "localhost")
    db_port: str = getenv("DB_PORT", "5432")
    db_name: str = getenv("DB_NAME", "postgres")

    return f"{db_dialect}://{db_user}:{db_password}@{db_ip}:{db_port}/{db_name}"


class DBConnectionHandler:
    @staticmethod
    def create_session(*, write=False, db_url: str) -> scoped_session[Session | Any]:
        engine = create_engine(
            db_url, pool_size=250, max_overflow=50, pool_use_lifo=True, pool_pre_ping=True, pool_recycle=300
        )

        if write:
            return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

        return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    # def read_unity_type_by_id(self, id_: uuid.UUID) -> Optional[UnityTypeDTO]:
    #     with Session(self.__engine) as session:
    #         query = sa.select(UnityType).where(UnityType.id == id_)
    #         row = session.execute(query).first()
    #     if row is None:
    #         return None
    #     return self.__unity_type_to_dto(row.UnityType)
    # |
    # def read_unity_type_by_name(self, name: str) -> Optional[UnityTypeDTO]:
    #     with Session(self.__engine) as session:
    #         query = sa.select(UnityType).where(UnityType.name == name)
    #         row = session.execute(query).first()
    #     if row is None:
    #         return None
    #     return self.__unity_type_to_dto(row.UnityType)
    #
    # def read_all_unity_types(self) -> list[UnityTypeDTO]:
    #     with Session(self.__engine) as session:
    #         query = sa.select(UnityType).order_by(UnityType.name)
    #         rows = session.execute(query).all()
    #
    #     return [self.__unity_type_to_dto(row.UnityType) for row in rows]
    #
    # def read_all_default_categorys(self) -> list[DefaultCategoryDTO]:
    #     with Session(self.__engine) as session:
    #         query = sa.select(DefaultCategory).order_by(DefaultCategory.name)
    #         rows = session.execute(query).all()
    #
    #     return [self.__default_category_to_dto(row.DefaultCategory) for row in rows]

    #
    # def __test_connection(self) -> None:
    #     retries, max_retries = 0, 5
    #     while retries < max_retries:
    #         try:
    #             with self.__engine.connect() as connection:
    #                 connection.execute(sa.text("SELECT 1"))
    #                 return
    #         except OperationalError as e:
    #             retries += 1
    #             print(f"Retrying ({retries}/{max_retries}) due to error: {e}")
    #             time.sleep(5)
    #     raise Exception("Database connection error after multiple retries.")

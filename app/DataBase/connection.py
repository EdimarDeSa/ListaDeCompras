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

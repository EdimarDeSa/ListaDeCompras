import time
import uuid
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.Models.dto_models import UserDTO, NewUser, UnityTypeDTO, DefaultCategoryDTO
from app.Models.models import User, UnityType, DefaultCategory


class DBConnectionHandler:
    def __init__(self, db_url: str) -> None:
        self.__engine: Engine = self.__create_engine(db_url)

        self.__test_connection()

    def create_user(self, new_user: NewUser) -> None:
        with Session(self.__engine) as session:
            user = User(**new_user.model_dump())

            session.add(user)
            session.commit()

    def read_user_by_id(self, id_: uuid.UUID) -> Optional[UserDTO]:
        with Session(self.__engine) as session:
            query = sa.select(User).where(User.id == id_)
            row = session.execute(query).first()
        if row is None:
            return None
        return self._user_to_dto(row.User)

    def read_unity_type_by_id(self, id_: uuid.UUID) -> Optional[UnityTypeDTO]:
        with Session(self.__engine) as session:
            query = sa.select(UnityType).where(UnityType.id == id_)
            row = session.execute(query).first()
        if row is None:
            return None
        return self._unity_type_to_dto(row.UnityType)

    def read_unity_type_by_name(self, name: str) -> Optional[UnityTypeDTO]:
        with Session(self.__engine) as session:
            query = sa.select(UnityType).where(UnityType.name == name)
            row = session.execute(query).first()
        if row is None:
            return None
        return self._unity_type_to_dto(row.UnityType)

    def read_all_users(self) -> list[UserDTO]:
        with Session(self.__engine) as session:
            query = sa.select(User).order_by(User.name)
            rows = session.execute(query).all()

        return [self._user_to_dto(row.User) for row in rows]

    def read_all_unity_types(self) -> list[UnityTypeDTO]:
        with Session(self.__engine) as session:
            query = sa.select(UnityType).order_by(UnityType.name)
            rows = session.execute(query).all()

        return [self._unity_type_to_dto(row.UnityType) for row in rows]

    def read_all_default_categorys(self) -> list[DefaultCategoryDTO]:
        with Session(self.__engine) as session:
            query = sa.select(DefaultCategory).order_by(DefaultCategory.name)
            rows = session.execute(query).all()

        return [self._default_category_to_dto(row.DefaultCategory) for row in rows]

    def update_user(self, user_dto: UserDTO) -> None:
        with Session(self.__engine) as session:
            query = sa.update(User).where(User.id == user_dto.id).values(**user_dto.model_dump())
            session.execute(query)
            session.commit()

    def delete_user_by_email(self, email: str) -> Optional[bool]:
        with Session(self.__engine) as session:
            query_read = sa.select(User).where(User.email == email)
            row = session.execute(query_read).first()

            if row is None:
                return None

            query_delete = sa.delete(User).where(User.email == email)
            session.execute(query_delete)

            session.commit()
        return True

    def __test_connection(self) -> None:
        retries, max_retries = 0, 5
        while retries < max_retries:
            try:
                with self.__engine.connect() as connection:
                    connection.execute(sa.text("SELECT 1"))
                    return
            except OperationalError as e:
                retries += 1
                print(f"Retrying ({retries}/{max_retries}) due to error: {e}")
                time.sleep(5)
        raise Exception("Database connection error after multiple retries.")

    @staticmethod
    def __create_engine(url: str) -> Engine:
        return sa.create_engine(url=url)

    @staticmethod
    def _user_to_dto(user: User) -> UserDTO:
        return UserDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            birthdate=user.birthdate,
            language=user.language,
            creation=user.creation,
            last_update=user.last_update,
        )

    @staticmethod
    def _unity_type_to_dto(unity_type: UnityType) -> UnityTypeDTO:
        return UnityTypeDTO(
            id=unity_type.id,
            name=unity_type.name,
            creation=unity_type.creation,
            last_update=unity_type.last_update,
            base_calc=unity_type.base_calc,
        )

    @staticmethod
    def _default_category_to_dto(unity_type: UnityType) -> DefaultCategoryDTO:
        return DefaultCategoryDTO(
            id=unity_type.id,
            name=unity_type.name,
            creation=unity_type.creation,
            last_update=unity_type.last_update,
        )

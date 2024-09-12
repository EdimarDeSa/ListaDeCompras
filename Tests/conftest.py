from Models.models import User
from faker import Faker
from fastapi.testclient import TestClient
from pytest import fixture

from DataBase.connection_handler import DBConnectionHandler, get_db_url
from DataBase.models.dto_models import UserDTO
from Enums.enums import LangEnum
from main import app


@fixture(scope="module")
def client():
    return TestClient(app)


@fixture(scope="module")
def fake_data() -> Faker:
    return Faker()


@fixture
def create_valid_user_data(fake_data: Faker) -> dict:
    return dict(
        id=fake_data.uuid4(),
        name=fake_data.name(),
        email=fake_data.email(),
        password=fake_data.password(),
        birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
        language=fake_data.enum(LangEnum),
    )


@fixture
def moc_user(create_valid_user_data) -> UserDTO:
    session = DBConnectionHandler.create_session(write=True, db_url=get_db_url())

    user = User(**create_valid_user_data)

    session.add(user)
    session.commit()

    yield UserDTO.model_validate(user)

    session.delete(user)
    session.commit()
    session.close()


def create_valid_user_data_new() -> dict:
    fake_data = Faker()
    return dict(
        id=fake_data.uuid4(),
        name=fake_data.name(),
        email=fake_data.email(),
        password=fake_data.password(),
        birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
        language=fake_data.enum(LangEnum),
    )


@fixture
def temporary_populate_db(client):
    session = DBConnectionHandler.create_session(write=True, db_url=get_db_url())

    users = [User(**create_valid_user_data_new()) for _ in range(9)]
    session.add_all(users)
    session.commit()

    yield [UserDTO.model_validate(user) for user in users]

    for user in users:
        session.delete(user)
    session.commit()
    session.close()

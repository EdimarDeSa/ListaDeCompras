from faker import Faker
from fastapi.testclient import TestClient
from pydantic import ValidationError
from pytest import raises, fixture

from app.Enums.enums import MessagesEnum, LangEnum
from app.Models.dto_models import NewUser, UserDTO
from main import app


class TestUser:
    @fixture
    def fake_data(self) -> Faker:
        return Faker()

    @fixture
    def valid_new_user(self, fake_data):
        return NewUser(
            id=fake_data.uuid4(),
            name=fake_data.name(),
            email=fake_data.email(),
            password=fake_data.password(),
            birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            language=fake_data.enum(LangEnum),
        )

    def test_create_new_user_success(self, valid_new_user):
        assert valid_new_user

    def test_create_userdto_success(self, fake_data):
        user_dto = UserDTO(
            name=fake_data.name(),
            email=fake_data.email(),
            birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
        )
        assert user_dto

    def test_create_new_user_fails_in_password_length(self, fake_data):
        with raises(ValidationError) as exec_info:
            NewUser(
                name=fake_data.name(),
                email=fake_data.email(),
                password=fake_data.password(length=7),
                birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            )

        assert exec_info.match(MessagesEnum.PASSWORD_LENGTH)
        assert exec_info.errisinstance(ValueError)

    def test_create_new_user_fails_in_password_number_digit(self, fake_data):
        with raises(ValidationError) as exec_info:
            NewUser(
                name=fake_data.name(),
                email=fake_data.email(),
                password=fake_data.password(digits=False),
                birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            )

        assert exec_info.match(MessagesEnum.PASSWORD_NEED_NUMBER)
        assert exec_info.errisinstance(ValueError)

    def test_create_new_user_fails_in_password_special(self, fake_data):
        with raises(ValidationError) as exec_info:
            NewUser(
                name=fake_data.name(),
                email=fake_data.email(),
                password=fake_data.password(special_chars=False),
                birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            )

        assert exec_info.match(MessagesEnum.PASSWORD_NEED_SPECIAL)
        assert exec_info.errisinstance(ValueError)

    def test_create_new_user_fails_in_password_null(self, fake_data):
        with raises(ValidationError) as exec_info:
            NewUser(
                name=fake_data.name(),
                email=fake_data.email(),
                password="",
                birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            )

        assert exec_info.match(MessagesEnum.PASSWORD_NULL)
        assert exec_info.errisinstance(ValueError)

    def test_create_new_user_fails_in_password_lower_case(self, fake_data):
        with raises(ValidationError) as exec_info:
            NewUser(
                name=fake_data.name(),
                email=fake_data.email(),
                password=fake_data.password(lower_case=False),
                birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            )

        assert exec_info.match(MessagesEnum.PASSWORD_NEED_LOWER_CASE)
        assert exec_info.errisinstance(ValueError)

    def test_create_new_user_fails_in_password_upper_case(self, fake_data):
        with raises(ValidationError) as exec_info:
            NewUser(
                name=fake_data.name(),
                email=fake_data.email(),
                password=fake_data.password(upper_case=False),
                birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            )

        assert exec_info.match(MessagesEnum.PASSWORD_NEED_UPPER_CASE)
        assert exec_info.errisinstance(ValueError)

    def test_create_new_user_fails_in_email_format(self, fake_data):
        with raises(ValidationError) as exec_info:
            NewUser(
                name=fake_data.name(),
                email="email",
                password=fake_data.password(upper_case=False),
                birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            )

        assert exec_info.errisinstance(ValueError)

    def test_create_userdto_fails_in_email_format(self, fake_data):
        with raises(ValidationError) as exec_info:
            NewUser(
                name=fake_data.name(),
                email="email",
                password=fake_data.password(upper_case=False),
                birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            )

        assert exec_info.errisinstance(ValueError)

    def test_create_new_user_fails_in_name_lenght(self, fake_data):
        with raises(ValidationError) as exec_info:
            NewUser(
                name="".join(["a" for _ in range(101)]),
                email=fake_data.email(),
                password=fake_data.password(upper_case=False),
                birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            )

        assert exec_info.errisinstance(ValueError)

    def test_create_userdto_fails_in_name_lenght(self, fake_data):
        with raises(ValidationError) as exec_info:
            UserDTO(
                name="".join(["a" for _ in range(101)]),
                email=fake_data.email(),
                birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            )

        assert exec_info.errisinstance(ValueError)


class TestUserController:
    @fixture
    def fake_data(self) -> Faker:
        return Faker()

    @fixture
    def valid_new_user(self, fake_data):
        return NewUser(
            id=fake_data.uuid4(),
            name=fake_data.name(),
            email=fake_data.email(),
            password=fake_data.password(),
            birthdate=fake_data.date_of_birth(maximum_age=80, minimum_age=18),
            language=fake_data.enum(LangEnum),
        )

    @fixture
    def client(self):
        return TestClient(app)

    @fixture
    def moc_user(self, client):
        response1 = client.get("/users/all")
        data: dict = response1.json()[0]
        return UserDTO(**data)

    def test_get_all_users(self, client):
        response = client.get("/users/all")

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_user_by_id_seccess(self, client, moc_user):
        response = client.get(f"/users/{moc_user.id}")

        assert response.status_code == 200
        assert response.json()["name"] == moc_user.name

    # def test_put_user_new_email_success(self, client, moc_user, fake_data):
    #     last_email = moc_user.email
    #     new_email = fake_data.email()
    #     updated_user = UserDTO(**moc_user.model_dump())
    #     updated_user.email = new_email
    #
    #     response = client.put(f"/users/", json=updated_user.model_dump_json())
    #
    #     assert response.status_code == 204
    #
    #     updated_user.email = last_email
    #
    #     response = client.put(f"/users/", json=updated_user.model_dump_json())
    #
    #     assert response.status_code == 204

    # def test_post_new_user(self, client, valid_new_user):
    #     new_user = valid_new_user
    #
    #     response = client.post("/users/", json=new_user.model_dump_json())
    #
    #     assert response.status_code == 201

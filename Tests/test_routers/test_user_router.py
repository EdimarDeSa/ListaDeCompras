import uuid

from app.Models.models import User
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete

from app.DataBase.connection import DBConnectionHandler, get_db_url
from app.DataBase.models.dto_models import UserDTO
from app.Enums.enums import ResponseCode
from app.Utils.global_functions import MsgLoader

"""
Estrutura padrão:

Arrange: setup de dependências e objetos para testes

Act: realiza a requisição para obter o resultado

Assert: valida o resultado e faz a validação de status

Cleanup: limpa o que foi feito no arrange quando necessário
"""


def test_get_all_users__success(client, temporary_populate_db):
    """Funciona mesmo com o banco já populado"""
    users = [user.name for user in temporary_populate_db]

    response = client.get("/users/all")

    json_data = response.json()
    users_data = [data["name"] for data in json_data["data"]]

    assert response.status_code == 200
    assert json_data["rc"] == 0
    assert len(users_data) >= len(users)
    assert all([user in users_data for user in users])


def test_get_user_by_id__success(client, moc_user):
    response = client.get(f"/users/{moc_user.id}")

    json_data = response.json()
    user_model = UserDTO.model_validate(json_data["data"])

    assert response.status_code == 200
    assert json_data["rc"] == ResponseCode.OK
    assert user_model == moc_user


def test_get_user_by_id__fail(client):
    id_to_fail = uuid.uuid4()
    response = client.get(f"/users/{id_to_fail}")

    json_data = response.json()
    msg = MsgLoader.get_message(ResponseCode.USER_NOT_FOUND)

    assert response.status_code == 404
    assert json_data["rc"] == ResponseCode.USER_NOT_FOUND
    assert json_data["data"] == msg


def test_post_new_user__success(client, create_valid_user_data):
    new_user = create_valid_user_data.copy()

    response = client.post("/users/", json=jsonable_encoder(new_user))

    json_data = response.json()

    assert 201 == response.status_code
    assert ResponseCode.OK == json_data["rc"]
    assert UserDTO(**new_user) == UserDTO(**json_data["data"])

    session = DBConnectionHandler.create_session(db_url=get_db_url())
    query = delete(User).where(User.email == new_user["email"])

    session.execute(query)
    session.commit()

    session.close()


def assert_error(response, rc: ResponseCode) -> None:
    msg = MsgLoader.get_message(rc)

    json_data = response.json()

    assert response.status_code == 400
    assert json_data["rc"] == rc
    assert json_data["data"] == msg


def test_post_new_user__fails_in_password_length(client, create_valid_user_data, fake_data):
    new_user = create_valid_user_data
    new_user.update({"password": fake_data.password(length=5)})

    response = client.post("/users/", json=jsonable_encoder(new_user))

    assert_error(response, ResponseCode.PASSWORD_LENGTH)


def test_post_new_user__fails_in_password_number_digit(client, create_valid_user_data, fake_data):
    new_user = create_valid_user_data
    new_user.update({"password": fake_data.password(digits=False)})

    response = client.post("/users/", json=jsonable_encoder(new_user))

    assert_error(response, ResponseCode.PASSWORD_NEED_NUMBER)


def test_post_new_user__fails_in_password_special(client, create_valid_user_data, fake_data):
    new_user = create_valid_user_data
    new_user.update({"password": fake_data.password(special_chars=False)})

    response = client.post("/users/", json=jsonable_encoder(new_user))

    assert_error(response, ResponseCode.PASSWORD_NEED_SPECIAL_CHAR)


def test_post_new_user__fails_in_password_blank(client, create_valid_user_data, fake_data):
    new_user = create_valid_user_data
    new_user.update({"password": ""})

    response = client.post("/users/", json=jsonable_encoder(new_user))

    assert_error(response, ResponseCode.PASSWORD_NULL)


def test_post_new_user__fails_in_password_lower_case(client, create_valid_user_data, fake_data):
    new_user = create_valid_user_data
    new_user.update({"password": fake_data.password(lower_case=False)})

    response = client.post("/users/", json=jsonable_encoder(new_user))

    assert_error(response, ResponseCode.PASSWORD_NEED_LOWER_CASE)


def test_post_new_user__fails_in_password_upper_case(client, create_valid_user_data, fake_data):
    new_user = create_valid_user_data
    new_user.update({"password": fake_data.password(upper_case=False)})

    response = client.post("/users/", json=jsonable_encoder(new_user))

    assert_error(response, ResponseCode.PASSWORD_NEED_UPPER_CASE)


def test_post_new_user__fails_in_email_format(client, create_valid_user_data, fake_data):
    new_user = create_valid_user_data
    new_user.update({"email": "email"})

    response = client.post("/users/", json=jsonable_encoder(new_user))

    assert_error(response, ResponseCode.EMAIL_INVALID)


def test_post_new_user__fails_in_name_length_too_long(client, create_valid_user_data, fake_data):
    new_user = create_valid_user_data
    new_user.update({"name": "".join(["a" for _ in range(101)])})

    response = client.post("/users/", json=jsonable_encoder(new_user))

    assert_error(response, ResponseCode.NAME_LENGTH)


def test_post_new_user__fails_in_name_length_too_short(client, create_valid_user_data, fake_data):
    new_user = create_valid_user_data
    new_user.update({"name": "".join(["a" for _ in range(2)])})

    response = client.post("/users/", json=jsonable_encoder(new_user))

    assert_error(response, ResponseCode.NAME_LENGTH)


def test_post_new_user__fails_in_name_length_blank(client, create_valid_user_data, fake_data):
    new_user = create_valid_user_data
    new_user.update({"name": ""})

    response = client.post("/users/", json=jsonable_encoder(new_user))

    assert_error(response, ResponseCode.NAME_LENGTH)


def test_put_user_new_email_success(client, moc_user, fake_data):
    new_email = fake_data.email()
    to_update = {"id": moc_user.id, "email": new_email}

    response = client.put(f"/users/", json=jsonable_encoder(to_update))

    json_data = response.json()

    assert response.status_code == 202
    assert json_data["rc"] == ResponseCode.OK


def test_delete_user_by_email_success(client, moc_user):
    user_email = moc_user.email

    response = client.delete(f"/users/{user_email}")

    json_data = response.json()

    assert response.status_code == 202
    assert json_data["rc"] == ResponseCode.OK


def test_delete_user_by_email_fail(client, moc_user, fake_data):
    user_email = fake_data.email()

    response = client.delete(f"/users/{user_email}")

    json_data = response.json()

    assert response.status_code == 404
    assert json_data["rc"] == ResponseCode.USER_NOT_FOUND

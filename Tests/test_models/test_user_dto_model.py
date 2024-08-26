from pydantic import ValidationError
from pytest import raises

from app.Models.dto_models import UserDTO


def test_create_userdto_success(create_valid_user_data):
    assert UserDTO.model_validate(create_valid_user_data)


def test_create_userdto_fails_in_email_format(create_valid_user_data):
    with raises(ValidationError) as exec_info:
        user = create_valid_user_data.update({"email": "email"})
        UserDTO.model_validate(user)

    assert exec_info.errisinstance(ValueError)


def test_create_userdto_fails_in_name_lenght(create_valid_user_data, fake_data):
    with raises(ValidationError) as exec_info:
        user_data = create_valid_user_data.update({"name": "".join(["a" for _ in range(101)])})
        UserDTO.model_validate(user_data)

    assert exec_info.errisinstance(ValueError)

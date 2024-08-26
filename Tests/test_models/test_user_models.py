from app.Models.dto_models import NewUser


def test_create_new_user_success(create_valid_user_data):
    assert NewUser.model_validate(create_valid_user_data)

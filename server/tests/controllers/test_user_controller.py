from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status
from icecream import ic

from app.controllers.users import UserController
from app.models.user import User

mock_queries = MagicMock()
uc = UserController(user_queries=mock_queries)

valid_user_data = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john@doe.com",
    },
    {"id": 2, "name": "Jane Doe", "email": "jane@doe.com", "sub": "1234567890"},
]

invalid_user_data = [
    {
        "id": 1,
        "name": "Jack Doe",
    }
]


def mock_select_one_by_id(id: int):
    for user in valid_user_data:
        if user.get("id") == id:
            return user
    return None


def mock_select_one_by_email(email: str):
    for user in valid_user_data:
        if user.get("email") == email:
            return user
    return None


def mock_select_one_by_sub(sub: str):
    for user in valid_user_data:
        if user.get("sub") == sub:
            return user
    return None


mock_queries.select_one_by_id = mock_select_one_by_id
mock_queries.select_one_by_email = mock_select_one_by_email
mock_queries.select_one_by_sub = mock_select_one_by_sub


def test_type():
    """Tests the type of the controller object."""
    assert isinstance(uc, UserController)


def test_get_users():
    """Tests the retrieval of users from the database."""
    mock_queries.select_all.return_value = valid_user_data
    users = uc.get_users()
    assert isinstance(users, list)
    assert len(users) == 2
    sub_found = False
    none_sub_found = False
    for user in users:
        assert isinstance(user, User)
        if user.sub:
            sub_found = True
            assert isinstance(user.sub, str)
        else:
            none_sub_found = True
    u1, u2 = users
    assert u1.id == 1
    assert u1.name == "John Doe"
    assert isinstance(u1.email, str)
    assert u2.id == 2
    assert u2.name == "Jane Doe"
    assert isinstance(u2.email, str)
    assert sub_found and none_sub_found


def test_get_users_sad():
    """Tests the retrieval of users from the database with invalid data."""
    mock_queries.select_all.return_value = invalid_user_data
    with pytest.raises(HTTPException) as e:
        uc.get_users()
    assert isinstance(e.value, HTTPException)
    assert e.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_get_user_by_id():
    """Tests the retrieval of a user by id from the database."""

    user = uc.get_user_by_id(1)
    assert isinstance(user, User)


def test_get_user_by_invalid_id():
    """Tests the retrieval of a user by id from the database with invalid data."""

    with pytest.raises(HTTPException) as e:
        uc.get_user_by_id(10)
    assert isinstance(e.value, HTTPException)
    assert e.value.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_by_email():
    """Tests the retrieval of a user by email from the database."""

    user = uc.get_user_by_email(valid_user_data[0]["email"])
    assert isinstance(user, User)


def test_get_user_by_invalid_email():
    """Tests the retrieval of a user by email from the database with invalid data."""

    with pytest.raises(HTTPException) as e:
        uc.get_user_by_email("carol@cat.com")
    assert isinstance(e.value, HTTPException)
    assert e.value.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_by_sub():
    """Tests the retrieval of a user by sub from the database."""

    user = uc.get_user_by_sub(valid_user_data[1]["sub"])
    assert isinstance(user, User)


def test_get_user_by_invalid_sub():
    """Tests the retrieval of a user by sub from the database with invalid data."""

    with pytest.raises(HTTPException) as e:
        uc.get_user_by_sub("123abc")
    assert isinstance(e.value, HTTPException)
    assert e.value.status_code == status.HTTP_404_NOT_FOUND

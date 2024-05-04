from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status
from icecream import ic

from app.controllers.group import GroupController
from app.models.group import Group

mock_queries = MagicMock()
gc = GroupController(group_queries=mock_queries)

valid_group_data = {
    "id": 1,
    "name": "Test Group",
    "bio": "Test Bio",
}

invalid_group_data = {
    "id": 1,
    "name": "Test Group",
}


def test_type():
    """Tests the type of the controller object."""
    assert isinstance(gc, GroupController)


def test_get_group():
    """Tests the retrieval of a group from the database with valid data."""
    mock_queries.select_one_by_id.return_value = valid_group_data
    group = gc.get_group()
    assert isinstance(group, Group)
    assert group.id == 1
    assert group.name == "Test Group"
    assert group.bio == "Test Bio"


def test_get_group_failure():
    """Tests a failure during the retrieval process or if the group is not found."""
    mock_queries.select_one_by_id.return_value = invalid_group_data
    with pytest.raises(HTTPException) as e:
        gc.get_group()
    assert isinstance(e.value, HTTPException)
    assert e.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_update_group_bio():
    """This test does not test updating of the bio, but rather tests that the corresponding
    method in the queries module is called with the correct arguments.
    """
    new_bio = "New Bio"
    mock_queries.update_group_bio = MagicMock()
    mock_queries.select_one_by_id.return_value = valid_group_data

    group = gc.update_group_bio(new_bio)
    MagicMock.assert_called_once_with(mock_queries.update_group_bio, new_bio)
    assert isinstance(group, Group)

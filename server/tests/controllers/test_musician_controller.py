from unittest.mock import Mock

import pytest
from fastapi import HTTPException, UploadFile, status
from icecream import ic

from app.controllers.musicians import MusicianController
from app.models.musician import Musician

mock_queries = Mock()
mc = MusicianController(musician_queries=mock_queries)

sample_data = [
    {
        "id": 1,
        "name": "John Doe",
        "bio": "A musician",
        "headshot_id": "headshot123",
    },
    {
        "id": 2,
        "name": "Jane Doe",
        "bio": "Another musician",
        "headshot_id": "headshotABC",
    },
]

bad_data = [
    # no bio
    {
        "id": "three",
        "name": "Jack Doe",
        "headshot_id": "headshot456",
    }
]


def mock_select_all_series():
    return sample_data


def mock_select_all_series_sad():
    return bad_data


def mock_select_one_by_id(musician_id: int):
    for musician in sample_data:
        if musician.get("id") == musician_id:
            return musician
    return None


mock_queries.select_all_series = mock_select_all_series
mock_queries.select_one_by_id = mock_select_one_by_id


def test_type():
    assert isinstance(mc, MusicianController)


"""
TODO: write tests for following methods:

- _update_musician_headshot
- _update_musician_bio
- _upload_headshot
"""


def test_happy_get_musicians():
    musicians = mc.get_musicians()
    assert isinstance(musicians, list)
    assert len(musicians) == 2
    for musician in musicians:
        assert isinstance(musician, Musician)
    m1, m2 = musicians
    assert m1.id == 1
    assert m1.name == "John Doe"
    assert m1.bio == "A musician"
    assert m1.headshot_id == "headshot123"
    assert m2.id == 2
    assert m2.name == "Jane Doe"
    assert m2.bio == "Another musician"
    assert m2.headshot_id == "headshotABC"


def test_sad_get_musicians():
    mock_queries.select_all_series = mock_select_all_series_sad
    with pytest.raises(HTTPException) as e:
        mc.get_musicians()
    mock_queries.select_all_series = mock_select_all_series
    assert isinstance(e.value, HTTPException)
    assert e.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_happy_get_musician():
    musician = mc.get_musician(1)
    assert isinstance(musician, Musician)
    assert musician.id == 1
    assert musician.name == "John Doe"
    assert musician.bio == "A musician"
    assert musician.headshot_id == "headshot123"


def test_musician_not_found():
    with pytest.raises(HTTPException) as e:
        mc.get_musician(3)
    assert isinstance(e.value, HTTPException)
    assert e.value.status_code == status.HTTP_404_NOT_FOUND
    assert e.value.detail == "Musician not found"

from unittest.mock import MagicMock

import pytest

from app.controllers.controller import MainController
from app.models.event import EventSeries, NewEventSeries
from app.models.musician import Musician

mock_user_controller = MagicMock()
mock_musician_controller = MagicMock()
mock_group_controller = MagicMock()
mock_event_controller = MagicMock()
mock_oauth_token = MagicMock()

mock_oauth_token.email_and_sub = MagicMock(return_value=("email", "sub"))

mock_token = MagicMock()

controller = MainController(
    user_controller=mock_user_controller,
    musicians_controller=mock_musician_controller,
    group_controller=mock_group_controller,
    event_controller=mock_event_controller,
    oauth_token=mock_oauth_token,  # type: ignore
)


def test_type():
    """Tests the type of the controller object."""
    assert isinstance(controller, MainController)


@pytest.mark.asyncio
async def test_get_musicians():
    """Tests the get_musicians method."""
    await controller.get_musicians()
    MagicMock.assert_called_once_with(mock_musician_controller.get_musicians)


@pytest.mark.asyncio
async def test_get_musician():
    """Tests the get_musician method."""
    musician_id = 1
    await controller.get_musician(musician_id)
    MagicMock.assert_called_once_with(
        mock_musician_controller.get_musician, musician_id
    )


@pytest.mark.asyncio
async def test_update_musician():
    """Tests the update_musician method.
    Underlying controller methods are tested elsewhere. This test is to ensure the method is called correctly.
    """
    musician = Musician(
        id=1, name="John Doe", bio="A musician", headshot_id="headshot123"
    )

    await controller.update_musician(
        musician=musician, url_param_id=1, token=mock_token
    )
    MagicMock.assert_called_with(mock_oauth_token.email_and_sub, mock_token)
    MagicMock.assert_called_once(mock_user_controller.get_user_by_sub)
    MagicMock.assert_called_once(mock_musician_controller.update_musician)


@pytest.mark.asyncio
async def test_get_events():
    """Tests the get_events method."""
    await controller.get_events()
    MagicMock.assert_called_once(mock_event_controller.get_all_series)


@pytest.mark.asyncio
async def test_get_event():
    """Tests the get_event method."""
    series_id = 1
    await controller.get_event(series_id)
    MagicMock.assert_called_once_with(
        mock_event_controller.get_one_series_by_id, series_id
    )


@pytest.mark.asyncio
async def test_create_event():
    """Tests the create_event method."""
    series = NewEventSeries(name="Test Event", description="A test event", events=[])
    await controller.create_event(series, mock_token)
    MagicMock.assert_called_with(mock_oauth_token.email_and_sub, mock_token)
    MagicMock.assert_called(mock_user_controller.get_user_by_sub)
    MagicMock.assert_called(mock_event_controller.create_series)


@pytest.mark.asyncio
async def test_add_series_poster():
    """Tests the add_series_poster method."""
    series_id = 1
    poster = MagicMock()
    await controller.add_series_poster(series_id, poster, mock_token)
    MagicMock.assert_called_with(mock_oauth_token.email_and_sub, mock_token)
    MagicMock.assert_called(mock_user_controller.get_user_by_sub)
    MagicMock.assert_called(mock_event_controller.add_series_poster)


@pytest.mark.asyncio
async def test_delete_series():
    """Tests the delete_series method."""
    series_id = 1
    await controller.delete_series(series_id, mock_token)
    MagicMock.assert_called_with(mock_oauth_token.email_and_sub, mock_token)
    MagicMock.assert_called(mock_user_controller.get_user_by_sub)
    MagicMock.assert_called(mock_event_controller.delete_series)


@pytest.mark.asyncio
async def test_update_series():
    """Tests the update_series method."""
    series = EventSeries(
        series_id=1, name="Test Event", description="A test event", events=[]
    )
    await controller.update_series(1, series, mock_token)
    MagicMock.assert_called_with(mock_oauth_token.email_and_sub, mock_token)
    MagicMock.assert_called(mock_user_controller.get_user_by_sub)
    MagicMock.assert_called(mock_event_controller.update_series)


@pytest.mark.asyncio
async def test_get_users():
    """Tests the get_users method."""
    await controller.get_users()
    MagicMock.assert_called_once(mock_user_controller.get_users)


@pytest.mark.asyncio
async def test_get_user():
    """Tests the get_user method."""
    user_id = 1
    await controller.get_user(user_id)
    MagicMock.assert_called_once_with(mock_user_controller.get_user_by_id, user_id)


@pytest.mark.asyncio
async def test_create_user():
    """Tests the create_user method."""
    await controller.create_user(mock_token)
    MagicMock.assert_called_with(mock_oauth_token.email_and_sub, mock_token)
    MagicMock.assert_called(mock_user_controller.create_user)


@pytest.mark.asyncio
async def test_get_group():
    """Tests the get_group method."""
    await controller.get_group()
    MagicMock.assert_called_once(mock_group_controller.get_group)


@pytest.mark.asyncio
async def test_update_group_bio():
    """Tests the update_group_bio method."""
    bio = "A new bio"
    await controller.update_group(bio, mock_token)
    MagicMock.assert_called_with(mock_oauth_token.email_and_sub, mock_token)
    MagicMock.assert_called(mock_user_controller.get_user_by_sub)
    MagicMock.assert_called(mock_group_controller.update_group_bio)

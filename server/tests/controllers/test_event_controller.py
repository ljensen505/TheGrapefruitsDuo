from datetime import datetime
from unittest.mock import MagicMock

from pydantic import HttpUrl
import pytest

from app.controllers.events import EventController
from app.models.event import Event, EventSeries

mock_queries = MagicMock()
ec = EventController(event_queries=mock_queries)

eventbrite_url = "https://www.eventbrite.com/e/the-grapefruits-duo-presents-works-for-horn-and-piano-tickets-1234567890"
medford = "Medford, OR"
newport_church = "First Presbyterian Church Newport"
eugene_church = "First Church of Christ, Scientist, Eugene"
map_url = "https://maps.app.goo.gl/hNfN8X5FBZLg8LDF8"


def test_type():
    assert isinstance(ec, EventController)


def test_all_series_with_no_data():
    """Tests with absent data."""

    def no_series() -> list[dict]:
        return []

    mock_queries.select_all = no_series
    result = ec.get_all_series()
    assert result == []


def test_all_series_with_basic_data():
    """Tests a single valid row with no event info"""

    def one_series_with_no_events() -> list[dict]:
        return [
            {
                "name": "Test Series",
                "description": "Test Description",
                "series_id": 1,
                "poster_id": "abc123",
            }
        ]

    mock_queries.select_all = one_series_with_no_events
    result = ec.get_all_series()
    assert isinstance(result, list)
    assert len(result) == 1
    series = result[0]
    assert isinstance(series, EventSeries)
    assert series.name == "Test Series"
    assert series.description == "Test Description"
    assert series.series_id == 1
    assert series.poster_id == "abc123"
    assert series.events == []


def test_all_series_with_detailed_data():
    """Tests a single valid row with event info"""

    series_id = 1
    series_name = "The Grapefruits Duo Presents: Works for Horn and Piano"
    series_description = "Pieces by Danzi, Gomez, Gounod, Grant, and Rusnak!"
    poster_id = "The_Grapefruits_Present_qhng6y"

    def one_series_with_events() -> list[dict]:

        row_1 = {
            "series_id": series_id,
            "name": series_name,
            "description": series_description,
            "poster_id": poster_id,
            "event_id": 1,
            "location": medford,
            "time": "2024-05-31 19:00:00.000",
            "ticket_url": eventbrite_url,
        }
        row_2 = {
            "series_id": series_id,
            "name": series_name,
            "description": series_description,
            "poster_id": poster_id,
            "event_id": 2,
            "location": newport_church,
            "time": "2024-06-16 16:00:00.000",
            "map_url": map_url,
        }
        row_3 = {
            "series_id": series_id,
            "name": series_name,
            "description": series_description,
            "poster_id": poster_id,
            "event_id": 3,
            "location": eugene_church,
            "time": "2024-06-23 15:00:00.000",
        }
        return [
            row_1,
            row_2,
            row_3,
        ]

    mock_queries.select_all = one_series_with_events
    result = ec.get_all_series()
    assert isinstance(result, list)
    assert len(result) == 1
    series = result[0]
    assert isinstance(series, EventSeries)
    assert series.name == series_name
    assert series.description == series_description
    assert series.series_id == series_id
    assert series.poster_id == poster_id
    events = series.events
    assert len(events) == 3

    for e in events:
        assert isinstance(e, Event)
        assert e.location is not None
        assert isinstance(e.time, datetime)
        assert e.event_id is not None
        if e.map_url is not None:
            assert isinstance(e.map_url, HttpUrl)
        if e.ticket_url is not None:
            assert isinstance(e.ticket_url, HttpUrl)

    e1, e2, e3 = events
    assert e1.event_id == 1
    assert e2.event_id == 2
    assert e3.event_id == 3
    assert e1.location == medford
    assert e2.location == newport_church
    assert e3.location == eugene_church
    assert str(e1.ticket_url) == eventbrite_url
    assert e2.ticket_url is None
    assert e3.ticket_url is None
    assert e1.map_url is None
    assert str(e2.map_url) == map_url
    assert e3.map_url is None
    assert e1.time == datetime(2024, 5, 31, 19, 0)
    assert e2.time == datetime(2024, 6, 16, 16, 0)
    assert e3.time == datetime(2024, 6, 23, 15, 0)


def test_all_series_with_many_series():
    """Tests multiple series with no events."""

    def many_series() -> list[dict]:
        return [
            {
                "name": "Test Series",
                "description": "Test Description",
                "series_id": 1,
                "poster_id": "abc123",
            },
            {
                "name": "Test Series 2",
                "description": "Test Description 2",
                "series_id": 2,
                "poster_id": "def456",
            },
            {
                "name": "Test Series 3",
                "description": "Test Description 3",
                "series_id": 3,
                "poster_id": "ghi789",
            },
        ]

    mock_queries.select_all = many_series
    result = ec.get_all_series()
    assert isinstance(result, list)
    assert len(result) == 3
    for series in result:
        assert isinstance(series, EventSeries)
        assert series.events == []


def test_all_series_with_error():
    """Tests an error during the retrieval process."""

    mock_log_error = MagicMock()
    ec.log_error = mock_log_error

    def invalid_series() -> list[dict]:
        # no series name
        return [
            {
                "description": "Test Description",
                "series_id": 1,
                "poster_id": "abc123",
            }
        ]

    mock_queries.select_all = invalid_series
    with pytest.raises(Exception):
        ec.get_all_series()
        MagicMock.assert_called_once(mock_log_error)


def test_one_series():
    def one_series_no_events(series_id: int) -> list[dict]:
        return [
            {
                "series_id": series_id,
                "name": "Test Series",
                "description": "Test Description",
                "poster_id": "abc123",
            }
        ]

    mock_queries.select_one_by_id = one_series_no_events
    series = ec.get_one_series_by_id(1)
    assert isinstance(series, EventSeries)
    assert series.name == "Test Series"
    assert series.description == "Test Description"
    assert series.series_id == 1
    assert series.poster_id == "abc123"
    assert series.events == []


def test_one_series_with_events():
    def one_series_with_events(series_id: int) -> list[dict]:
        return [
            {
                "series_id": series_id,
                "name": "Test Series",
                "description": "Test Description",
                "poster_id": "abc123",
                "event_id": 1,
                "location": medford,
                "time": "2024-05-31 19:00:00.000",
                "ticket_url": eventbrite_url,
            },
            {
                "series_id": series_id,
                "name": "Test Series",
                "description": "Test Description",
                "poster_id": "abc123",
                "event_id": 2,
                "location": newport_church,
                "time": "2024-06-16 16:00:00.000",
                "map_url": map_url,
            },
            {
                "series_id": series_id,
                "name": "Test Series",
                "description": "Test Description",
                "poster_id": "abc123",
                "event_id": 3,
                "location": eugene_church,
                "time": "2024-06-23 15:00:00.000",
            },
        ]

    mock_queries.select_one_by_id = one_series_with_events
    series = ec.get_one_series_by_id(1)
    assert isinstance(series, EventSeries)
    assert series.name == "Test Series"
    assert series.description == "Test Description"
    assert series.series_id == 1
    assert series.poster_id == "abc123"
    events = series.events
    assert len(events) == 3
    for event in events:
        assert isinstance(event, Event)

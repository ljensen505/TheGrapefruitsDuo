from unittest.mock import Mock

import pytest
from icecream import ic

from app.controllers.musicians import MusicianController
from app.models.musician import Musician

mock_queries = Mock()
ec = MusicianController(musician_queries=mock_queries)


def test_type():
    assert isinstance(ec, MusicianController)


# TODO: Write tests for MusicianController

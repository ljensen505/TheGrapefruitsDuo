from .events import EventQueries
from .group import GroupQueries
from .musicians import MusicianQueries
from .users import UserQueries

event_queries = EventQueries()
user_queries = UserQueries()
musician_queries = MusicianQueries()
group_queries = GroupQueries()

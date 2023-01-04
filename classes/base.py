import string
from datetime import datetime, timedelta

from config.formats import DATETIME_FORMAT
from classes.enums import Role, BanType
import json


class Ban:
    """Class for ban representation"""
    def __init__(self, ban_id: int = None, user_id: int = None, is_active: bool = True, cause: str = None,
                 from_user: int = None, ban_starts: datetime | str = None, ban_duration: int = None,
                 ban_ends: datetime | str = None):
        self.__id = ban_id
        self.__user_id = user_id
        self.__is_active = is_active
        self.__cause = cause
        self.__from_user = from_user
        self.__ban_starts = ban_starts if type(ban_starts) == datetime else datetime.strptime(ban_starts, DATETIME_FORMAT)
        self.__ban_ends = self.calculate_unban_time(self.__ban_starts, ban_duration) if ban_ends is None else (ban_ends if type(ban_ends) == datetime else datetime.strptime(ban_starts, DATETIME_FORMAT))

    @property
    def id(self) -> int:
        """Database id"""
        return self.__id

    @staticmethod
    def calculate_unban_time(start_ban_time, ban_duration: int) -> datetime:
        """Calculate unban time with start ban time, and it's duration. Mostly for internal usage"""
        return start_ban_time + timedelta(seconds=ban_duration)

    @property
    def user_id(self) -> int:
        """Database id of banned user"""
        return self.__user_id

    @property
    def cause(self) -> str:
        """Ban cause"""
        return self.__cause

    @property
    def ban_starts(self):
        """Time of ban receiving"""
        return self.__ban_starts

    @property
    def ban_ends(self) -> datetime:
        """Time of ban termination (can be devalued by ban duration)"""
        return self.__ban_ends

    @property
    def ban_duration(self) -> int:
        """Difference between start and end of ban, virtual parameter (if equals with -1, means permanent ban)"""
        return (self.__ban_ends - self.__ban_starts).seconds

    @ban_duration.setter
    def ban_duration(self, new_ban_duration) -> None:
        """Set difference between start and end of ban"""
        self.__ban_ends = self.calculate_unban_time(self.__ban_starts, new_ban_duration)

    def check_ban_relevance(self) -> bool:
        """Check that start time is earlier than end time and ban state is active"""
        return (self.__ban_ends < self.__ban_starts or datetime.now() < self.__ban_ends or self.ban_duration < 0) and self.active

    @property
    def ban_type(self) -> BanType:
        """Type of ban, represented of BanType enum"""
        return BanType.PERMANENT if self.ban_duration == -1 else BanType.TEMPORARY

    @property
    def active(self) -> bool:
        """Ban state"""
        return self.__is_active

    @active.setter
    def active(self, state) -> None:
        """Set ban state"""
        self.__is_active = state

    @property
    def from_user(self) -> int:
        """Database id of moderator, who appointed a ban"""
        return self.__from_user

    @from_user.setter
    def from_user(self, from_user: int):
        """Set id of moderator"""
        self.__from_user = from_user

    def ban_starts_str(self) -> str:
        """Get string representation of start ban time"""
        return self.__ban_starts.strftime(DATETIME_FORMAT)

    def ban_ends_str(self) -> str:
        """Get string representation of end ban time"""
        return self.__ban_ends.strftime(DATETIME_FORMAT)


class Joke:
    """Class for joke representation"""
    def __init__(self, joke_id: int = None, user_id: int = None, data: str = None, on_review: bool = True,
                 tags: list[str] | str = None, added_at: datetime | str = None):
        self.__id = joke_id
        self.__user_id = user_id
        self.__data = data
        self.__on_review = on_review
        self.__tags = tags if type(tags) == list[str] else (tags.split(" ") if type(tags) == str else None)
        self.__added_at = added_at if type(added_at) == datetime else datetime.strptime(added_at, DATETIME_FORMAT)

    @property
    def id(self) -> int:
        """Database id"""
        return self.__id

    @property
    def user_id(self) -> int:
        """Database id of user, who added current joke"""
        return self.__user_id

    @property
    def data(self) -> str:
        """Joke text"""
        return self.__data

    @property
    def on_review(self) -> bool:
        """Joke state"""
        return self.__on_review

    @on_review.setter
    def on_review(self, new_state: bool) -> None:
        """Set joke state"""
        self.__on_review = new_state

    @property
    def tags(self) -> list[str]:
        """Tags, associated with current joke"""
        return self.__tags

    @tags.setter
    def tags(self, new_tags: list[str]) -> None:
        """Set joke tags"""
        self.__tags = new_tags

    def tags_str(self) -> str:
        """String representation of tags (mostly for database)"""
        return " ".join(self.__tags)

    @property
    def added_at(self) -> datetime:
        """Time, when current joke was added"""
        return self.__added_at

    @added_at.setter
    def added_at(self, added_at) -> None:
        """Set time, when current joke was added"""
        self.__added_at = added_at

    def added_at_str(self) -> str:
        """String representation of time, when current joke was added"""
        return self.__added_at.strftime(DATETIME_FORMAT)

    def to_json(self):
        """Convert current joke to JSON like string (for possible API)"""
        return json.JSONEncoder().encode({'data': self.__data,
                                          'tags': self.__tags,
                                          'added_at': self.added_at_str()})


class Like:
    """Class for like representation"""
    def __init__(self, like_id: int = None, user_id: int = None, joke_id: int = None):
        self.__like_id = like_id
        self.__user_id = user_id
        self.__joke_id = joke_id

    @property
    def id(self) -> int:
        """Database id"""
        return self.__like_id

    @property
    def user_id(self) -> int:
        """Database user id"""
        return self.__user_id

    @property
    def joke_id(self) -> int:
        """Database joke id"""
        return self.__joke_id


class User:
    """Class for user representation"""
    def __init__(self, user_id: int = None, tg_id: int = None, username: str = None, first_name: str = None,
                 last_name: str = None, role: Role | str = None):
        self.__id = user_id
        self.__tg_id = tg_id
        self.__username = username
        self.__first_name = first_name
        self.__last_name = last_name
        self.__role = role if type(role) == Role else (Role.role_from_string(role) if role else None)

    @property
    def id(self) -> int:
        """Database id"""
        return self.__id

    @property
    def tg_id(self) -> int:
        """Telegram internal id"""
        return self.__tg_id

    @property
    def username(self) -> str:
        """Username"""
        return self.__username

    @username.setter
    def username(self, new_username) -> None:
        """Set username"""
        self.__username = new_username

    @property
    def first_name(self) -> str:
        """First name"""
        return self.__first_name

    @first_name.setter
    def first_name(self, new_first_name) -> None:
        """Set first name"""
        self.__first_name = new_first_name

    @property
    def last_name(self) -> str:
        """Last name"""
        return self.__last_name

    @last_name.setter
    def last_name(self, new_last_name) -> None:
        """Set last name"""
        self.__last_name = new_last_name

    @property
    def role(self) -> Role:
        """User role, represented with Role enum"""
        return self.__role

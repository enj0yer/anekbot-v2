from datetime import datetime, timedelta
from enums import Role


class Ban:
    def __init__(self, ban_id: int = None, user_id: int = None, is_active: bool = True, cause: str = None, from_user: int = None, ban_starts: datetime = None, ban_duration: int = None, ban_ends: datetime = None):
        self.__id = ban_id
        self.__user_id = user_id
        self.__is_active = is_active
        self.__cause = cause
        self.__from_user = from_user
        self.__ban_starts = ban_starts
        self.__ban_ends = self.calculate_unban_time(ban_starts, ban_duration) if ban_ends is None else ban_ends

    @property
    def id(self) -> int:
        return self.__id

    @staticmethod
    def calculate_unban_time(start_ban_time, ban_duration: int) -> datetime:
        return start_ban_time + timedelta(seconds=ban_duration)

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def cause(self) -> str:
        return self.__cause

    @property
    def ban_starts(self):
        return self.__ban_starts

    @property
    def ban_ends(self) -> datetime:
        return self.__ban_ends

    @property
    def ban_duration(self) -> timedelta.seconds:
        return self.__ban_ends - self.__ban_starts

    @ban_duration.setter
    def ban_duration(self, new_ban_duration) -> None:
        self.__ban_ends = self.calculate_unban_time(self.__ban_starts, new_ban_duration)

    def check_ban_relevance(self) -> bool:
        return (self.__ban_ends < self.__ban_starts or datetime.now() < self.__ban_ends) and self.active

    @property
    def active(self) -> bool:
        return self.__is_active

    @active.setter
    def active(self, state) -> None:
        self.__is_active = state

    @property
    def from_user(self) -> int:
        return self.__from_user

    @from_user.setter
    def from_user(self, from_user: int):
        self.__from_user = from_user


class Joke:
    def __init__(self, joke_id: int = None, user_id: int = None, data: str = None, on_review: bool = True):
        self.__id = joke_id
        self.__user_id = user_id
        self.__data = data
        self.__on_review = on_review

    @property
    def id(self) -> int:
        return self.__id

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def data(self) -> str:
        return self.__data

    @property
    def on_review(self) -> bool:
        return self.__on_review

    @on_review.setter
    def on_review(self, new_state: bool) -> None:
        assert isinstance(new_state, bool), 'Parameter type must be bool'
        self.__on_review = new_state

    def __str__(self):
        return self.__data


class Like:
    def __init__(self, like_id: int = None, user_id: int = None, joke_id: int = None):
        self.__like_id = like_id
        self.__user_id = user_id
        self.__joke_id = joke_id

    @property
    def id(self) -> int:
        return self.__like_id

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def joke_id(self) -> int:
        return self.__joke_id


class User:
    def __init__(self, user_id: int = None, tg_id: int = None, username: str = None, first_name: str = None, last_name: str = None, role: Role = None):
        self.__id = user_id
        self.__tg_id = tg_id
        self.__username = username
        self.__first_name = first_name
        self.__last_name = last_name
        self.__role = role

    @property
    def id(self) -> int:
        return self.__id

    @property
    def tg_id(self) -> int:
        return self.__tg_id

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, new_username) -> None:
        self.__username = new_username

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, new_first_name) -> None:
        self.__first_name = new_first_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, new_last_name) -> None:
        self.__last_name = new_last_name

    @property
    def role(self) -> Role:
        return self.__role




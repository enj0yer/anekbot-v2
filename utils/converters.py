
from classes.base import Ban, User, Like, Joke


class DatabaseConverter:

    @staticmethod
    def convert_ban(_tuple: tuple) -> Ban:
        return Ban(ban_id=_tuple[0], user_id=_tuple[1], cause=_tuple[2], ban_starts=_tuple[3], ban_ends=_tuple[4],
                   is_active=_tuple[5], from_user=_tuple[6])

    @staticmethod
    def convert_user(_tuple: tuple) -> User:
        return User(user_id=_tuple[0], tg_id=_tuple[1], username=_tuple[2], first_name=_tuple[3], last_name=_tuple[4],
                    role=_tuple[5])

    @staticmethod
    def convert_like(_tuple: tuple) -> Like:
        return Like(like_id=_tuple[0], user_id=_tuple[1], joke_id=_tuple[2])

    @staticmethod
    def convert_joke(_tuple: tuple) -> Joke:
        return Joke(joke_id=_tuple[0], user_id=_tuple[1], data=_tuple[2], on_review=_tuple[3], tags=_tuple[4],
                    added_at=_tuple[5])

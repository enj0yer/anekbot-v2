import datetime

from aiogram import types

from bot.service import send_ban_info
from classes.base import Ban, User, Joke
from classes.connection import Connection
from classes.enums import Role


def __save_user_data(message: types.Message):
    user_controller = UsersController()
    user = user_controller.get_by_tg_id(message.from_user.id)
    if not user:
        user_controller.save(User(tg_id=message.from_user.id,
                                  username=message.from_user.username,
                                  first_name=message.from_user.first_name,
                                  last_name=message.from_user.last_name,
                                  role=Role.USER))
    else:
        user_controller.save(User(user_id=user.id,
                                  username=message.from_user.username,
                                  first_name=message.from_user.first_name,
                                  last_name=message.from_user.last_name))


def process_user(message: types.Message, save_changes: bool = False) -> bool:
    if save_changes:
        __save_user_data(message)

    ban = UsersController.is_banned(User(tg_id=message.from_user.id))
    if ban:
        send_ban_info(message, ban)
        return False
    return True


class BansController(Connection):
    """Class for bans controlling"""
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def save(self, user: User, ban: Ban) -> None:
        """Save (insert and disable other bans) ban"""
        self.disable_all_bans(user)
        self._cursor.execute(
            "insert into bans (user_id, cause, ban_starts, ban_ends, is_active, from_user) values "
            "((?), (?), (?), (?), (?), (?))", (user.id, ban.cause, ban.ban_starts_str(), ban.ban_ends_str(), ban.active, ban.from_user,)
        )
        self._connection.commit()

    def disable_ban(self, ban: Ban) -> None:
        """Disable current ban"""
        self._cursor.execute("update bans set is_active = 0 where id = (?)", (ban.id,))
        self._connection.commit()

    def disable_all_bans(self, user: User) -> None:
        """Disable all bans for current user"""
        self._cursor.execute("update bans set is_active = 0 where user_id = (?)", (user.id,))
        self._connection.commit()

    def find(self, user: User) -> list[Ban]:
        """Find all bans of current user"""
        raw_result = self._cursor.execute(
            "select id, user_id, cause, ban_starts, ban_ends, is_active, from_user from bans where user_id = (?) order by ban_starts, ban_ends",
            (user.id,)).fetchall()

        result = []

        for string in raw_result:
            result.append(
                Ban(ban_id=string[0], user_id=string[1], cause=string[2], ban_starts=string[3], ban_ends=string[4],
                    is_active=string[5], from_user=string[6]))

        return result

    def find_active(self, user: User) -> Ban:
        """Find active user ban (must be single)"""
        raw_result = self._cursor.execute(
            "select id, user_id, cause, ban_starts, ban_ends, is_active, from_user from bans where user_id = (?) and is_active",
            (user.id,)).fetchone()

        return Ban(ban_id=raw_result[0], user_id=raw_result[1], cause=raw_result[2], ban_starts=raw_result[3], ban_ends=raw_result[4], is_active=raw_result[5], from_user=raw_result[6])


class JokesController(Connection):
    """Class for jokes controlling"""
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def get_random_joke(self) -> Joke:
        """Get random joke (no guarantee against the same jokes in a row)"""
        result = self._cursor.execute(
            "select jokes.id, jokes.user_id, data, on_review, tags, added_at from jokes where on_review = 0 limit 1 offset abs(random() % (select count(*) from jokes));").fetchone()
        return Joke(joke_id=result[0], user_id=result[1], data=result[2], on_review=result[3], tags=result[4], added_at=result[5])

    def get_joke(self, joke: Joke) -> Joke:
        """Get current joke with joke id"""
        result = self._cursor.execute("select id, user_id, data, on_review, tags, added_at from jokes where id = (?)", (joke.id,))

        return Joke(joke_id=result[0], user_id=result[1], data=result[2], on_review=result[3], tags=result[4], added_at=result[5])

    def change_review_state(self, joke: Joke, on_review: bool) -> None:
        """Change review state of current joke"""
        self._cursor.execute("update jokes set on_review = (?) where id = (?)",
                             (on_review, joke.id,))
        self._connection.commit()

    def get_amounts_of_jokes(self, user: User) -> int:
        """Get amount of jokes, added by current user"""
        result = self._cursor.execute("select count(id) from jokes where user_id = (?) and on_review = 0",
                                      (user.id,)).fetchone()

        return result[0]

    def get_all_liked_jokes(self, user: User) -> list[Joke]:
        """Get all jokes, liked by current user"""
        raw_result = self._cursor.execute("select l.id, l.user_id, data, on_review, tags, added_at "
                                          "from jokes inner join likes l "
                                          "on jokes.id = l.joke_id and l.user_id = (?) where on_review = 0",
                                          (user.id,)).fetchall()

        result = []

        for raw_joke in raw_result:
            result.append(Joke(joke_id=raw_joke[0], user_id=raw_joke[1], data=raw_joke[2], on_review=raw_joke[3], tags=raw_joke[4], added_at=raw_joke[5]))

        return result

    def get_on_review_jokes(self):
        """Get all still not approved jokes"""
        raw_result = self._cursor.execute("select id, user_id, data, on_review, tags, added_at "
                                          "from jokes where on_review = 1").fetchall()

        result = []

        if not raw_result:
            for raw_joke in raw_result:
                result.append(Joke(joke_id=raw_joke[0], user_id=raw_joke[1], data=raw_joke[2], on_review=raw_joke[3], tags=raw_joke[4], added_at=raw_joke[5]))
        else:
            return raw_result

        return result


class LikesController(Connection):
    """Class for likes controlling"""
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def create_like(self, user: User, joke: Joke):
        """Add like"""
        self._cursor.execute("insert into likes (user_id, joke_id) values (?, ?)", (user.id, joke.id,))
        self._connection.commit()

    def delete_like(self, user: User, joke: Joke):
        """Delete like"""
        self._cursor.execute("delete from likes where user_id = (?) and joke_id = (?)", (user.id, joke.id,))
        self._connection.commit()

    def count_likes(self, joke: Joke):
        """Count likes on current joke"""
        result = self._cursor.execute("select count(id) from likes where joke_id = (?)", (joke.id,)).fetchone()
        return result[0]

    def check_like(self, user: User, joke: Joke) -> bool:
        """Check like on current joke from current user"""
        result = self._cursor.execute("select id from likes where user_id = (?) and joke_id = (?)", (user.id, joke.id,)).fetchone()
        return len(result) == 0


class UsersController(Connection):
    """Class for users controlling"""
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def get_admins_list(self) -> list[User]:
        """Get list of all admins"""
        result = self._cursor.execute(
            "select id, tg_id, username, first_name, last_name, role from users where role = 'ADMIN' or role = 'OWNER' order by username").fetchall()
        admin_list = []
        if not result:
            for string in result:
                admin_list.append(User(user_id=string[0],
                                       tg_id=string[1],
                                       username=string[2],
                                       first_name=string[3],
                                       last_name=string[4],
                                       role=string[5]))
        else:
            return result

        return admin_list

    def save(self, user: User) -> None:
        """Save new user or changes for existing user"""
        if user.id is None:
            self.__insert(user)
        else:
            self.__update(user)

    def __update(self, user: User) -> None:
        """Save changes for existing user"""
        self._cursor.execute("update users \
                              set tg_id = iif((?) is not null, (?), tg_id), \
                                  username = iif((?) is not null, (?), username), \
                                  first_name = iif((?) is not null, (?), first_name), \
                                  last_name = iif((?) is not null, (?), last_name), \
                                  role = iif((?) is not null, (?), role) \
                              where id = (?)", (user.tg_id, user.tg_id,
                                                user.username, user.username,
                                                user.first_name, user.first_name,
                                                user.last_name, user.last_name,
                                                user.role.name, user.role.name,
                                                user.id,))
        self._connection.commit()

    def __insert(self, user: User) -> None:
        """Save new user"""
        self._cursor.execute("insert into users (tg_id, username, first_name, last_name, role)"
                             "values ((?), (?), (?), (?), (?))", (user.tg_id, user.username, user.first_name, user.last_name, user.role.name,))
        self._connection.commit()

    def get_by_tg_id(self, tg_id: int) -> User:
        """Get user by telegram id"""
        result = self._cursor.execute("select id, tg_id, username, first_name, last_name, role from users where tg_id = (?)", (tg_id,)).fetchone()

        return result if not result else User(user_id=result[0], tg_id=result[1], username=result[2], first_name=result[3], last_name=result[4], role=result[5])

    def get_by_id(self, user_id: int) -> User:
        """Get user by database id"""
        result = self._cursor.execute("select id, tg_id, username, first_name, last_name, role from users where id = (?)", (user_id,)).fetchone()

        return result if not result else User(user_id=result[0], tg_id=result[1], username=result[2], first_name=result[3], last_name=result[4], role=result[5])

    @staticmethod
    def is_banned(user: User) -> Ban:
        """Check user ban state"""
        return BansController().find_active(user) if user.id is not None else BansController().find_active(UsersController().get_by_tg_id(user.id))

    @staticmethod
    def ban(user: User, from_user: int, cause: str, ban_duration: int) -> Ban:
        """Appoint ban to current user"""
        ban = Ban(user_id=user.id, from_user=from_user, cause=cause, ban_starts=datetime.datetime.now(), ban_duration=ban_duration)
        BansController().save(user, ban)

        return ban

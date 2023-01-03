import datetime

from base import Ban
from classes import Connection
from base import User
from base import Joke
from classes.enums import Role


class BansController(Connection):

    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def save(self, user: User, ban: Ban) -> None:
        self.disable_all_bans(user)
        self._cursor.execute(
            "insert into bans (user_id, cause, ban_starts, ban_ends, is_active, from_user)  values "
            "((?), (?), (?), (?), (?), (?))", (user.id, ban.cause, ban.ban_starts_str(), ban.ban_ends_str(), ban.active, ban.from_user,)
        )
        self._connection.commit()

    def disable_ban(self, ban: Ban) -> None:
        self._cursor.execute("update bans set is_active = 0 where id = (?)", (ban.id,))
        self._connection.commit()

    def disable_all_bans(self, user: User) -> None:
        self._cursor.execute("update bans set is_active = 0 where user_id = (?)", (user.id,))
        self._connection.commit()

    def find(self, user: User) -> list[Ban]:
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
        raw_result = self._cursor.execute(
            "select id, user_id, cause, ban_starts, ban_ends, is_active, from_user from bans where user_id = (?) and is_active",
            (user.id,)).fetchone()

        return Ban(ban_id=raw_result[0], user_id=raw_result[1], cause=raw_result[2], ban_starts=raw_result[3], ban_ends=raw_result[4], is_active=raw_result[5], from_user=raw_result[6])


class JokesController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def get_random_joke(self) -> Joke:
        result = self._cursor.execute(
            "select id, user_id, data, on_review from jokes limit 1 offset abs(random() % (select count(*) from jokes)) where on_review = 0;").fetchone()
        return Joke(result[0], result[1], result[2], result[3])

    def change_review_state(self, joke: Joke, on_review: bool) -> None:
        """ONLY IN DATABASE"""
        self._cursor.execute("update jokes set on_review = (?) where id = (?)",
                             (on_review, joke.id,))
        self._connection.commit()

    def get_amounts_of_jokes(self, user: User) -> int:
        result = self._cursor.execute("select count(id) from jokes where user_id = (?) and on_review = 0",
                                      (user.id,)).fetchone()

        return result[0]

    def get_all_liked_jokes(self, user: User) -> list[Joke]:
        raw_result = self._cursor.execute("select l.id, l.user_id, data, on_review "
                                          "from jokes inner join likes l "
                                          "on jokes.id = l.joke_id and l.user_id = (?) where on_review = 0",
                                          (user.id,)).fetchall()

        result = []

        for raw_joke in raw_result:
            result.append(Joke(joke_id=raw_joke[0], user_id=raw_joke[1], data=raw_joke[2], on_review=raw_joke[3]))

        return result

    def get_on_review_jokes(self):
        raw_result = self._cursor.execute("select id, user_id, data, on_review "
                                          "from jokes where on_review = 1 limit 10").fetchall()

        result = []

        for raw_joke in raw_result:
            result.append(Joke(joke_id=raw_joke[0], user_id=raw_joke[1], data=raw_joke[2], on_review=raw_joke[3]))

        return result


class LikesController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def create_like(self, user: User, joke: Joke):
        self._cursor.execute("insert into likes (user_id, joke_id) values (?, ?)", (user.id, joke.id,))
        self._connection.commit()

    def delete_like(self, user: User, joke: Joke):
        self._cursor.execute("delete from likes where user_id = (?) and joke_id = (?)", (user.id, joke.id,))
        self._connection.commit()

    def count_likes(self, joke: Joke):
        result = self._cursor.execute("select count(id) from likes where joke_id = (?)", (joke.id,)).fetchone()
        return result[0]


class UsersController(Connection):

    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def get_admins_list(self) -> list[User]:
        result = self._cursor.execute(
            "select id, tg_id, username, first_name, last_name, role from users where role = 'ADMIN' or role = 'OWNER' order by username asc").fetchall()
        admin_list = []
        for string in result:
            admin_list.append(User(user_id=string[0],
                                   tg_id=string[1],
                                   username=string[2],
                                   first_name=string[3],
                                   last_name=string[4],
                                   role=Role.role_from_string(string[5])))

        return admin_list

    def save(self, user: User) -> None:
        if user.id is None:
            self.__insert(user)
        else:
            self.__update(user)

    def __update(self, user: User) -> None:
        self._cursor.execute("update users \
                              set tg_id = iif((?) is not null, (?), tg_id), \
                                  username = iif((?) is not null, (?), username), \
                                  first_name = iif((?) is not null, (?), first_name), \
                                  last_name = iif((?) is not null, (?), last_name), \
                                  role = iif((?) is not null, (?), role), \
                              where id = (?)", (user.tg_id, user.tg_id,
                                                user.username, user.username,
                                                user.first_name, user.first_name,
                                                user.last_name, user.last_name,
                                                user.role.name, user.role.name,
                                                user.id,))
        self._connection.commit()

    def __insert(self, user: User) -> None:
        self._cursor.execute("insert into users (tg_id, username, first_name, last_name, role)"
                             "values ((?), (?), (?), (?), (?))", (user.tg_id, user.username, user.first_name, user.last_name, user.role.name,))
        self._connection.commit()

    def get_by_tg_id(self, tg_id: int) -> User:
        result = self._cursor.execute("select id, tg_id, username, first_name, last_name, role from users where tg_id = (?)", (tg_id,)).fetchone()

        return User(user_id=result[0], tg_id=result[1], username=result[2], first_name=result[3], last_name=result[4], role=Role.role_from_string(result[5]))

    def get_by_id(self, user_id: int) -> User:
        result = self._cursor.execute("select id, tg_id, username, first_name, last_name, role from users where id = (?)", (user_id,)).fetchone()

        return User(user_id=result[0], tg_id=result[1], username=result[2], first_name=result[3], last_name=result[4], role=Role.role_from_string(result[5]))

    @staticmethod
    def is_banned(user: User) -> Ban:
        bc = BansController()
        active_ban = bc.find_active(user)

        return active_ban

    @staticmethod
    def ban(user: User, from_user: int, cause: str, ban_duration: int) -> Ban:
        ban = None
        if ban_duration == -1:
            ban = Ban(user_id=user.id, from_user=from_user, cause=cause, ban_ends=datetime.datetime.now() - datetime.timedelta(days=1), ban_starts=datetime.datetime.now(), ban_duration=ban_duration)
        else:
            ban = Ban(user_id=user.id, from_user=from_user, cause=cause, ban_duration=ban_duration, ban_starts=datetime.datetime.now())
        bc = BansController()
        bc.save(user, ban)

        return ban



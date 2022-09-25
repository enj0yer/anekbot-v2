from classes.Ban import Ban
from classes.Connection import Connection
from classes.User import User


class BansController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def save(self, user: User, ban: Ban) -> None:
        if ban.id is None:
            self.__insert(user, ban)
        else:
            self.__update(user, ban)

    def __update(self, user: User, ban: Ban) -> None:
        self._cursor.execute("update users \
                                      set user_id = iif((?) is not null, (?), null), \
                                          cause = iif((?) is not null, (?), null), \
                                          ban_starts = iif((?) is not null, (?), null), \
                                          ban_ends = iif((?) is not null, (?), null), \
                                          is_active = iif((?) is not null, (?), null), \
                                      where id = (?)", (user.id, user.id,
                                                        ban.cause, ban.cause,
                                                        ban.ban_starts, ban.ban_starts,
                                                        ban.ban_ends, ban.ban_ends,
                                                        ban.active, ban.active,
                                                        ban.id,))
        self._connection.commit()

    def __insert(self, user: User, ban: Ban) -> None:
        self._cursor.execute("insert into users (user_id, cause, ban_starts, ban_ends, is_active)"
                             "values (?, ?, ?, ?)",
                             (user.id, ban.cause, ban.ban_starts, ban.ban_ends, ban.active,))
        self._connection.commit()

    def disable_ban(self, ban: Ban) -> None:
        self._cursor.execute("delete from bans where id = (?)", (ban.id,))
        self._connection.commit()

    def disable_all_bans(self, user: User) -> None:
        self._cursor.execute("update bans set is_active = 0 where user_id = (?)", (user.id,))
        self._connection.commit()

    def find(self, user: User) -> list[Ban]:
        raw_result = self._cursor.execute("select id, user_id, cause, ban_starts, ban_ends, is_active from bans where user_id = (?) order by ban_starts, ban_ends").fetchall()

        result = []

        for string in raw_result:
            result.append(Ban(ban_id=string[0], user_id=string[1], cause=string[2], ban_starts=string[3], ban_ends=string[4], is_active=string[5]))

        return result

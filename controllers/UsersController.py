from classes.Connection import Connection
from classes.User import User


class UsersController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def get_admins_list(self) -> list[User]:
        result = self._cursor.execute(
            "select id, tg_id, username, first_name, last_name, is_owner, is_admin from users where is_admin = 1 or is_owner = 1").fetchall()
        admin_list = []
        for string in result:
            admin_list.append(User(user_id=string[0],
                                   tg_id=string[1],
                                   username=string[2],
                                   first_name=string[3],
                                   last_name=string[4],
                                   is_owner=string[5],
                                   is_admin=string[6]))

        return admin_list

    def save(self, user: User) -> None:
        if user.user_id is None:
            self.__insert(user=user)
        else:
            self.__update(user)

    def __update(self, user: User) -> None:
        self._cursor.execute("update users \
                              set tg_id = iif((?) is not null, (?), null), \
                                  username = iif((?) is not null, (?), null), \
                                  first_name = iif((?) is not null, (?), null), \
                                  last_name = iif((?) is not null, (?), null), \
                                  is_owner = iif((?) is not null, (?), null), \
                                  is_admin = iif((?) is not null, (?), null) \
                              where id = (?)", (user.tg_id, user.tg_id,
                                                user.username, user.username,
                                                user.first_name, user.first_name,
                                                user.last_name, user.last_name,
                                                user.is_owner, user.is_owner,
                                                user.is_admin, user.is_admin,
                                                user.user_id,))

    def __insert(self, user: User) -> None:
        self._cursor.execute("insert into users (tg_id, username, first_name, last_name, is_owner, is_admin)"
                             "values (?, ?, ?, ?, ?, ?)", (user.tg_id, user.username, user.first_name, user.last_name, user.is_owner, user.is_admin,))

    def get_by_tg_id(self, tg_id: int) -> User:
        result = self._cursor.execute("select id, tg_id, username, first_name, last_name, is_owner, is_admin from users where tg_id = (?)", (tg_id,)).fetchone()

        return User(user_id=result[0], tg_id=result[1], username=result[2], first_name=result[3], last_name=result[4], is_owner=result[5], is_admin=result[6])
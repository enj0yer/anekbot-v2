from classes.Connection import Connection
from classes.User import User


class UsersController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def get_admins_list(self) -> list[User]:
        result = self._cursor.execute("select id, tg_id, username, first_name, last_name, is_owner, is_admin from users where is_admin = 1 or is_owner = 1").fetchall()
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


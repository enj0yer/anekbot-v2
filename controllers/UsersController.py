from classes.Connection import Connection
from classes.User import User


class UsersController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def get_admins_list(self) -> list[User]:
        result = self._cursor.execute("select * from users where is_admin = 1 or is_owner = 1").fetchall()
        admin_list = []

        for string in result:
            admin_list.append(User(string[0], string[1], string[2], string[3], string[4], string[5]))

        return admin_list


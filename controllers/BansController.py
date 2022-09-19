from classes.Ban import Ban
from classes.Connection import Connection
from classes.User import User


class BansController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def add_new_ban(self, user: User, ban: Ban):
        self._cursor.execute("insert into bans (user_id, cause, unban_time) values (?, ?, ?)", (user.user_id, ban.))
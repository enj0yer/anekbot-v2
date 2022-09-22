from classes.Ban import Ban
from classes.Connection import Connection
from classes.User import User


class BansController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def add_new_ban(self, user: User, ban: Ban):
        self._cursor.execute("insert into bans (user_id, cause, ban_starts, ban_ends) values (?, ?, ?, ?)", (user.user_id, ban.cause, ban.ban_starts, ban.ban_ends,))

    def remove_ban(self, ban: Ban):
        self._cursor.execute("delete from bans where id = (?)", (ban.id,))


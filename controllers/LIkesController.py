from classes.Anekdot import Anekdot
from classes.Connection import Connection
from classes.User import User


class LikesController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def create_like(self, user: User, anekdot: Anekdot):
        self._cursor.execute("insert into likes (user_id, anekdot_id) values (?, ?)", (user.get_user_id(), anekdot.get_anekdot_id(),))

    def delete_like(self, user: User, anekdot: Anekdot):
        self._cursor.execute("delete from likes where user_id = (?) and anekdot_id = (?)", (user.get_user_id(), anekdot.get_anekdot_id(),))


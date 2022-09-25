from classes.Anekdot import Anekdot
from classes.Connection import Connection
from classes.User import User


class LikesController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def create_like(self, user: User, anekdot: Anekdot):
        self._cursor.execute("insert into likes (user_id, anekdot_id) values (?, ?)", (user.id, anekdot.id,))
        self._connection.commit()

    def delete_like(self, user: User, anekdot: Anekdot):
        self._cursor.execute("delete from likes where user_id = (?) and anekdot_id = (?)", (user.id, anekdot.id,))
        self._connection.commit()

    def count_likes(self, anekdot: Anekdot):
        result = self._cursor.execute("select count(id) from likes where anekdot_id = (?)", (anekdot.id,)).fetchone()
        return result[0]
from classes.Anekdot import Anekdot
from classes.Connection import Connection
from classes.User import User


class AnekdotsController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def get_random_anekdot(self) -> Anekdot:
        result = self._cursor.execute(
            "SELECT id, user_id, data, on_review from anekdots limit 1 offset abs(random() % (select count(*) from anekdots)) where on_review = 0;").fetchone()
        return Anekdot(result[0], result[1], result[2], result[3])

    def change_review_state(self, anekdot: Anekdot, on_review: bool) -> None:
        """ONLY IN DATABASE"""
        self._cursor.execute("update anekdots set on_review = (?) where id = (?)",
                             (on_review, anekdot.id,))
        self._connection.commit()

    def get_amounts_of_anekdots(self, user: User) -> int:
        result = self._cursor.execute("select count(id) from anekdots where user_id = (?) and on_review = 0", (user.id,)).fetchone()

        return result[0]

    def get_all_liked_anekdots(self, user: User) -> list[Anekdot]:
        raw_result = self._cursor.execute("select id, user_id, data, on_review "
                                          "from anekdots inner join likes l "
                                          "on anekdots.id = l.anekdot_id and l.user_id = (?) where on_review = 0", (user.id,)).fetchall()

        result = []

        for raw_anekdot in raw_result:
            result.append(Anekdot(anekdot_id=raw_anekdot[0], user_id=raw_anekdot[1], data=raw_anekdot[2], on_review=raw_anekdot[3]))

        return result

    def get_on_review_anekdots(self):
        raw_result = self._cursor.execute("select id, user_id, data, on_review "
                                          "from anekdots where on_review = 1 limit 10").fetchall()

        result = []

        for raw_anekdot in raw_result:
            result.append(Anekdot(anekdot_id=raw_anekdot[0], user_id=raw_anekdot[1], data=raw_anekdot[2], on_review=raw_anekdot[3]))

        return result
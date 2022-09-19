from classes.Anekdot import Anekdot
from classes.Connection import Connection


class AnekdotsController(Connection):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def get_random_anekdot(self) -> Anekdot:
        result = self._cursor.execute(
            "SELECT * from anekdots limit 1 offset abs(random() % (select count(*) from anekdots)) where on_review = 0;").fetchone()
        return Anekdot(result[0], result[1], result[2], result[3], result[4])

    def change_review_state(self, anekdot: Anekdot, on_review: bool) -> None:
        """ONLY IN DATABASE"""
        self._cursor.execute("update anekdots set on_review = (?) where id = (?)",
                             (on_review, anekdot.anekdot_id,))



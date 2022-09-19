class Anekdot:
    def __init__(self, anekdot_id: int = None, user_id: int = None, data: str = None, on_review: bool = True, amount_of_likes: int = 0):
        self.__id = anekdot_id
        self.__user_id = user_id
        self.__data = data
        self.__on_review = on_review
        self.__amount_of_likes = amount_of_likes

    @property
    def anekdot_id(self) -> int:
        return self.__id

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def data(self) -> str:
        return self.__data

    @property
    def on_review(self)  -> bool:
        return self.__on_review

    @property
    def amount_of_likes(self) -> int:
        return self.__amount_of_likes

    @on_review.setter
    def on_review(self, new_state: bool) -> None:
        assert isinstance(new_state, bool), 'Parameter type must be bool'
        self.__on_review = new_state

    def increase_likes(self) -> None:
        self.__amount_of_likes += 1

    def decrease_likes(self) -> None:
        self.__amount_of_likes -= 1

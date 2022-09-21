class Anekdot:
    def __init__(self, anekdot_id: int = None, user_id: int = None, data: str = None, on_review: bool = True):
        self.__id = anekdot_id
        self.__user_id = user_id
        self.__data = data
        self.__on_review = on_review

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

    @on_review.setter
    def on_review(self, new_state: bool) -> None:
        assert isinstance(new_state, bool), 'Parameter type must be bool'
        self.__on_review = new_state


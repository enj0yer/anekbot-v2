class Like:
    def __init__(self, like_id: int = None, user_id: int = None, anekdot_id: int = None):
        self.__like_id = like_id
        self.__user_id = user_id
        self.__anekdot_id = anekdot_id

    @property
    def like_id(self) -> int:
        return self.__like_id

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def anekdot_id(self) -> int:
        return self.like_id


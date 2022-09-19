from datetime import datetime, timedelta


class Ban:
    def __init__(self, ban_id: int = None, user_id: int = None, cause: str = None, ban_duration: int = None, ban_time: datetime = None, unban_time: datetime = None):
        assert isinstance(ban_id, int)
        self.__id = ban_id
        self.__user_id = user_id
        self.__cause = cause
        self.__ban_time = datetime.
        self.__unban_time = self.__calculate_unban_date(ban_duration)

    @staticmethod
    def __calculate_unban_date(ban_duration: int) -> datetime:
        Ban.__test_ban_duration(ban_duration)
        return datetime.now() + timedelta(seconds=ban_duration)

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def cause(self) -> str:
        return self.__cause

    @property
    def unban_time(self) -> datetime:
        return self.__unban_time

    @property
    def ban_duration(self) -> int:
        return self.__ban_duration

    @ban_duration.setter
    def ban_duration(self, new_ban_duration) -> None:
        Ban.__test_ban_duration(new_ban_duration)
        self.__unban_time = self.__calculate_unban_date(new_ban_duration)
        self.__ban_duration = new_ban_duration

    @staticmethod
    def __test_ban_duration(ban_duration: int):
        assert isinstance(ban_duration, int), 'Parameter type must be int'
        assert ban_duration > 0, 'Parameter must be above zero'

    @staticmethod
    def __assert_constructor(ban_id: int, user_id: int, cause: str, ban_duration):

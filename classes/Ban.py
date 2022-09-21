from datetime import datetime, timedelta


class Ban:
    def __init__(self, ban_id: int = None, user_id: int = None, cause: str = None, ban_starts: datetime = None, ban_duration: int = None):
        self.__id = ban_id
        self.__user_id = user_id
        self.__cause = cause
        self.__ban_starts = ban_starts
        self.__ban_ends = self.__calculate_unban_time(ban_starts, ban_duration)

    @staticmethod
    def __calculate_unban_time(start_ban_time, ban_duration: int) -> datetime:
        return start_ban_time + timedelta(seconds=ban_duration)

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def cause(self) -> str:
        return self.__cause

    @property
    def start_ban_time(self):
        return self.__ban_starts

    @property
    def end_ban_time(self) -> datetime:
        return self.__ban_ends

    @property
    def ban_duration(self) -> timedelta.seconds:
        return self.__ban_ends - self.__ban_starts

    @ban_duration.setter
    def ban_duration(self, new_ban_duration) -> None:
        self.__ban_ends = self.__calculate_unban_time(self.__ban_starts, new_ban_duration)

    def check_ban_state(self):
        return datetime.now() < self.__ban_ends


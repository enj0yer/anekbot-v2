from datetime import datetime, timedelta


class Ban:
    def __init__(self, ban_id: int = None, user_id: int = None, is_active: bool = True, cause: str = None, ban_starts: datetime = None, ban_duration: int = None, ban_ends: datetime = None):
        self.__id = ban_id
        self.__user_id = user_id
        self.__is_active = is_active
        self.__cause = cause
        self.__ban_starts = ban_starts
        self.__ban_ends = self.calculate_unban_time(ban_starts, ban_duration) if ban_ends is None else ban_ends

    @property
    def id(self) -> int:
        return self.__id

    @staticmethod
    def calculate_unban_time(start_ban_time, ban_duration: int) -> datetime:
        return start_ban_time + timedelta(seconds=ban_duration)

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def cause(self) -> str:
        return self.__cause

    @property
    def ban_starts(self):
        return self.__ban_starts

    @property
    def ban_ends(self) -> datetime:
        return self.__ban_ends

    @property
    def ban_duration(self) -> timedelta.seconds:
        return self.__ban_ends - self.__ban_starts

    @ban_duration.setter
    def ban_duration(self, new_ban_duration) -> None:
        self.__ban_ends = self.calculate_unban_time(self.__ban_starts, new_ban_duration)

    def check_ban_relevance(self) -> bool:
        return (self.__ban_ends < self.__ban_starts or datetime.now() < self.__ban_ends) and self.active

    @property
    def active(self) -> bool:
        return self.__is_active

    @active.setter
    def active(self, state) -> None:
        self.__is_active = state
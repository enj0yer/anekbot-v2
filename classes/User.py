

class User:
    def __init__(self, user_id: int, tg_id: int, username: str, first_name: str, last_name: str, is_owner: bool, is_admin: bool, amount_of_anekdots: int):
        self.__id = user_id
        self.__tg_id = tg_id
        self.__username = username
        self.__first_name = first_name
        self.__last_name = last_name
        self.__is_owner = is_owner
        self.__is_admin = is_admin
        self.__aoa = amount_of_anekdots

    def get_user_id(self) -> int:
        return self.__id

    def get_tg_id(self) -> int:
        return self.__tg_id

    def get_username(self) -> str:
        return self.__username

    def is_owner(self) -> bool:
        return self.__is_owner

    def is_admin(self) -> bool:
        return self.__is_admin

    def get_amount_of_anekdots(self) -> int:
        return self.__aoa

    

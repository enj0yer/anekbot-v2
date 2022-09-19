

class User:
    def __init__(self, user_id: int = None, tg_id: int = None, username: str = None, first_name: str = None, last_name: str = None, is_owner: bool = False, is_admin: bool = False):
        self.__id = user_id
        self.__tg_id = tg_id
        self.__username = username
        self.__first_name = first_name
        self.__last_name = last_name
        self.__is_owner = is_owner
        self.__is_admin = is_admin

    @property
    def user_id(self) -> int:
        return self.__id

    @property
    def tg_id(self) -> int:
        return self.__tg_id

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, new_username) -> None:
        assert isinstance(new_username, str) and new_username is None, 'Parameter type must be str'
        self.__username = new_username

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, new_first_name) -> None:
        assert isinstance(new_first_name, str) and new_first_name is None, 'Parameter type must be str'
        self.__first_name = new_first_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, new_last_name) -> None:
        assert isinstance(new_last_name, str) or new_last_name is None, 'Parameter type must be str'
        self.__last_name = new_last_name

    @property
    def is_owner(self) -> bool:
        return self.__is_owner

    @property
    def is_owner(self, owner_state) -> None:
        """NOT FOR USAGE"""
        assert isinstance(owner_state, bool), 'Parameter type must be bool'
        self.__is_owner = owner_state

    @property
    def is_admin(self) -> bool:
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, admin_state: bool):
        assert isinstance(admin_state, bool), 'Parameter type must be bool'
        self.__is_admin = admin_state


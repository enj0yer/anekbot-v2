from enum import Enum


class Direction(Enum):
    INCREASE = 1
    DECREASE = 2


class Role(Enum):
    OWNER = "OWNER",
    ADMIN = "ADMIN",
    USER = "USER"

    @staticmethod
    def role_from_string(string_role: str):
        for value in Role.mro()[0]:
            if value.name == string_role.upper():
                return value

        else:
            return None

    def __str__(self):
        return self.name

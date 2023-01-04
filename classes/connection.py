import sqlite3
from config.settings import PATH


class Connection:

    def __init__(self):
        self._connection = sqlite3.connect(PATH)
        self._cursor = self._connection.cursor()

    def __del__(self):
        self._cursor.close()
        self._connection.close()


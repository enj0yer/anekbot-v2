

class Anekdot:
    def __init__(self, anekdot_id: int, user_id: int, data: str, on_review: bool, amount_of_likes: int):
        self.__id = anekdot_id
        self.__user_id = user_id
        self.__data = data
        self.__on_review = on_review
        self.__amount_of_likes = amount_of_likes

    def get_anekdot_id(self):
        return self.__id

    def get_user_id(self):
        return self.__user_id

    def get_data(self):
        return self.__data

    def on_review(self):
        return self.__on_review

    def get_amount_of_likes(self):
        return self.__amount_of_likes

    def change_review_state(self, new_state: bool):
        self.__on_review = new_state

    def increase_likes(self):
        self.__amount_of_likes += 1

    def decrease_likes(self):
        self.__amount_of_likes -= 1

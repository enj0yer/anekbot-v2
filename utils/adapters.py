
from classes.base import Ban, User, Like, Joke


class DatabaseAdapter:

    @staticmethod
    def adapt_ban(ban: Ban) -> tuple:
        return ban.user_id, ban.cause, ban.ban_starts_str(), ban.ban_ends_str(), ban.active, ban.from_user,

    @staticmethod
    def adapt_user(user: User) -> tuple:
        return user.tg_id, user.username, user.first_name, user.last_name, user.role,

    @staticmethod
    def adapt_like(like: Like) -> tuple:
        return like.user_id, like.joke_id,

    @staticmethod
    def adapt_joke(joke: Joke) -> tuple:
        return joke.user_id, joke.data, joke.on_review, joke.tags_str(), joke.added_at_str(),

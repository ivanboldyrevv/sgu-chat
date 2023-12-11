from website.db import get_db

from website.repo.repositories.post_repository import PostRepository
from website.repo.repositories.comment_repository import CommentsRepository
from website.repo.repositories.user_repository import UserRepository
from website.repo.repositories.statistics_repository import StatisticsRepository
from website.repo.repositories.bookmark_repository import BookmarkRepository
from website.repo.repositories.like_repository import LikeRepository
from website.repo.repositories.chat_repository import ChatRepository


class RepositoryFactory:
    def __init__(self):
        self.db = get_db()

    def create_post_repository(self):
        return PostRepository(self.db)

    def create_comments_repository(self):
        return CommentsRepository(self.db)

    def create_user_repository(self):
        return UserRepository(self.db)

    def create_statistics_repository(self):
        return StatisticsRepository(self.db)

    def create_bookmark_repository(self):
        return BookmarkRepository(self.db)

    def create_likes_repository(self):
        return LikeRepository(self.db)

    def create_chat_repository(self):
        return ChatRepository(self.db)

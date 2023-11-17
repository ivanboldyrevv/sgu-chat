from website.db import get_db
import os
from flask import request
from werkzeug.utils import secure_filename


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
        return Statistics(self.db)

    def create_bookmark_repository(self):
        return Bookmark(self.db)

    def create_likes_repository(self):
        return Like(self.db)

    def create_chat_repository(self):
        return Chat(self.db)


class PostRepository:
    def __init__(self, db):
        self.db = db

    def get_posts(self):
        return self.db.execute(
            'SELECT post.*, user.*, user.id as user_id, GROUP_CONCAT(files_post.filename) AS filenames, stats.* '
            'FROM post '
            'JOIN user ON post.author_id = user.id '
            'JOIN files_post ON post.id = files_post.post_id '
            'JOIN posts_statistics AS stats ON post.id = stats.id '
            'GROUP BY post.id '
            'ORDER BY post.created DESC').fetchall()

    def post_to_db(self, title, data, author):
        self.db.execute('INSERT INTO post (title, data, author_id) VALUES (?, ?, ?)', (title, data, author))
        post_id = self.db.execute('SELECT id FROM post ORDER BY created DESC').fetchone()[0]
        self.db.execute('INSERT INTO posts_statistics (views, post_id) VALUES (?, ?)', (0, post_id,))
        self.db.commit()

    def files_to_db(self, filename, file_type):
        post_id = self.db.execute('SELECT id FROM post ORDER BY created DESC').fetchone()['id']
        self.db.execute('INSERT INTO files_post (filename, filetype, post_id) VALUES (?, ?, ?)',
                        (filename, file_type, post_id), )
        self.db.commit()

    def get_post(self, post_id):
        return self.db.execute('SELECT post.*, user.*, GROUP_CONCAT(files_post.filename) AS filenames, stats.* '
                               'FROM post '
                               'JOIN user ON post.author_id = user.id '
                               'JOIN files_post ON post.id = files_post.post_id '
                               'JOIN posts_statistics AS stats ON post.id = stats.id '
                               'WHERE post.id = ?', (post_id,)).fetchone()

    def subscribe(self, user_id, subscription):
        self.db.execute('INSERT INTO subscribers (user_id, subscription) VALUES (?, ?)', (user_id, subscription))
        self.db.commit()

    def unsubscribe(self, user_id, subscription):
        self.db.execute('DELETE FROM subscribers WHERE user_id = ? AND subscription = ?', (user_id, subscription))
        self.db.commit()

    def check_sub(self, user_id, subscription):
        return True if self.db.execute('SELECT * FROM subscribers WHERE user_id = ? AND subscription = ?',
                                       (user_id, subscription)).fetchone() is not None else False


class CommentsRepository:
    def __init__(self, db):
        self.db = db

    def comment_to_db(self, data, post_id, author_id):
        self.db.execute('INSERT INTO comments (data, post_id, author_id) VALUES (?, ?, ?)', (data, post_id, author_id))
        self.db.commit()

    def get_comments(self, post_id):
        return self.db.execute(
            'SELECT * FROM comments JOIN user ON comments.author_id = user.id WHERE post_id = ? ORDER BY created DESC',
            (post_id,)).fetchall()


class UserRepository:
    def __init__(self, db):
        self.db = db
        self.path = 'website/static/users_files'

    def change_settings(self, user_id):
        file = request.files['user-avatar']
        filename = secure_filename(file.filename)
        file.save(os.path.join(self.path, filename))
        self.db.execute('UPDATE user SET avatar = ? WHERE id = ?', (filename, user_id))
        self.db.commit()

    def render_profile(self, username):
        return self.db.execute('SELECT * FROM user WHERE username = ? ', (username,)).fetchone()

    def user_posts(self, user_id):
        return self.db.execute('SELECT * FROM post WHERE author_id = ? ORDER BY created DESC ', (user_id,)).fetchall()

    def call_request(self, friend_1, friend_2):
        self.db.execute('INSERT INTO friendlist (status, friend_1, friend_2) VALUES (?, ?, ?)',
                        ('request', friend_1, friend_2))
        self.db.commit()

    def recall_request(self, friend_1, friend_2):
        self.db.execute('DELETE FROM friendlist WHERE status = ? AND friend_1 = ? AND friend_2 = ?',
                        ('request', friend_1, friend_2))
        self.db.commit()

    def check_request(self, f, friend_1, friend_2=None):
        if f == 'recall':
            return self.db.execute('SELECT * FROM friendlist WHERE status = ? AND friend_1 = ? AND friend_2 = ?',
                                   ('request', friend_1, friend_2)).fetchone()
        elif f == 'get':
            return self.db.execute('SELECT * FROM friendlist JOIN user ON friendlist.friend_1 = user.id '
                                   'WHERE status = ? AND friend_2 = ? ',
                                   ('request', friend_1)).fetchall()

    def update_status(self, status, friend_1, friend_2):
        self.db.execute('UPDATE friendlist SET status = ? WHERE friend_1 = ? AND friend_2 = ?',
                        (status, friend_1, friend_2))
        self.db.commit()

    def get_friends(self, user_id):
        return self.db.execute('SELECT user.*, user.id AS user_id FROM friendlist '
                               'JOIN user ON CASE '
                               'WHEN status = ? AND friend_1 = ? THEN friendlist.friend_2 = user.id '
                               'WHEN status = ? AND friend_2 = ? THEN friendlist.friend_1 = user.id '
                               'END',
                               ('friendship', user_id, 'friendship', user_id)).fetchall()


class Statistics:
    def __init__(self, db):
        self.db = db

    def update_views(self, post_id, views):
        self.db.execute('UPDATE posts_statistics SET views = ? WHERE post_id = ?', (views, post_id))
        self.db.commit()

    def update_likes(self, post_id):
        self.db.execute('UPDATE posts_statistics '
                        'SET likes = (SELECT COUNT(*) FROM likes WHERE post_id = ?) '
                        'WHERE post_id = ?', (post_id, post_id))
        self.db.commit()

    def get_view(self, post_id):
        return self.db.execute('SELECT views FROM posts_statistics WHERE post_id = ?', (post_id,)).fetchone()[0]


class Bookmark:
    def __init__(self, db):
        self.db = db

    def add_bookmark(self, user_id, post_id):
        self.db.execute('INSERT INTO bookmarks (post_id, user_id) VALUES (?, ?)', (post_id, user_id))
        self.db.commit()

    def remove_bookmark(self, user_id, post_id):
        self.db.execute('DELETE FROM bookmarks WHERE post_id = ? AND user_id = ?', (post_id, user_id))
        self.db.commit()

    def check_bookmark(self, user_id, post_id):
        return True if self.db.execute('SELECT * FROM bookmarks WHERE post_id = ? '
                                       'AND user_id = ?', (post_id, user_id)).fetchone() is not None else False

    def get_bookmarks(self, user_id):
        return self.db.execute('SELECT post.* FROM bookmarks '
                               'JOIN (SELECT post.*, user.*, GROUP_CONCAT(files_post.filename) AS filenames '
                               'FROM post '
                               'JOIN user ON post.author_id = user.id '
                               'JOIN files_post ON post.id = files_post.post_id '
                               'GROUP BY post.id ) AS post ON bookmarks.post_id = post.id '
                               'WHERE bookmarks.user_id = ?', (user_id,)).fetchall()


class Like:
    def __init__(self, db):
        self.db = db

    def add_like(self, post_id, user_id):
        self.db.execute('INSERT INTO likes (post_id, user_id) VALUES (?, ?)', (post_id, user_id))
        self.db.commit()

    def remove_like(self, post_id, user_id):
        self.db.execute('DELETE FROM likes WHERE post_id = ? AND user_id = ?', (post_id, user_id))
        self.db.commit()

    def check_like(self, post_id, user_id):
        return True if self.db.execute('SELECT * FROM likes WHERE post_id = ? AND user_id = ?',
                                       (post_id, user_id)).fetchone() is not None else False


class Chat:
    def __init__(self, db):
        self.db = db

    def add_group(self, friend_1, friend_2):
        self.db.execute('INSERT INTO groups (name) VALUES (?)', ('friend_1, friend_2',))
        group_id = self.db.execute('SELECT id FROM groups ORDER BY create_date DESC').fetchone()[0]
        self.db.execute('INSERT INTO user_group (user_id, group_id) VALUES (?, ?), (?, ?)',
                        (friend_1, group_id, friend_2, group_id))
        self.db.commit()

    def get_groups(self, user_id):
        return self.db.execute(
            'SELECT *, groups.id AS group_id FROM user_group '
            'JOIN groups ON user_group.group_id = groups.id '
            'JOIN user ON user_group.user_id = user.id '
            'WHERE group_id IN (SELECT group_id FROM user_group WHERE user_id = ?) AND user_id <> ?',
            (user_id, user_id)).fetchall()

    def message_to_db(self, user_id, group_id, message):
        self.db.execute(
            'INSERT INTO messages (data, creator_id) VALUES (?, ?)',
            (message, user_id))

        self.db.execute(
            'INSERT INTO message_recipient (recipient_id, recipient_group_id, message_id) '
            'VALUES (?, ?, (SELECT id FROM messages ORDER BY create_date DESC LIMIT 1))',
            (user_id, group_id))

        self.db.commit()

    def get_messages(self, group_id):
        return self.db.execute('SELECT * FROM message_recipient '
                               'JOIN messages ON message_recipient.message_id = messages.id '
                               'JOIN user ON message_recipient.recipient_id = user.id '
                               'WHERE recipient_group_id = ?', (group_id,)).fetchall()

    def return_to_chat_from_friendlist(self, first, second):
        return self.db.execute('SELECT groups.id '
                               'FROM groups '
                               'JOIN user_group ON groups.id = user_group.group_id '
                               'WHERE user_id IN (?, ?) '
                               'GROUP BY groups.id '
                               'HAVING COUNT(DISTINCT user_id) = 2', (first, second)).fetchone()[0]

    def show_last_message(self, group_id):
        return self.db.execute('SELECT data, username FROM message_recipient '
                               'JOIN messages ON message_recipient.message_id = messages.id '
                               'JOIN user ON messages.creator_id = user.id '
                               'WHERE recipient_group_id = ? '
                               'ORDER BY messages.create_date DESC', (group_id,)).fetchone()

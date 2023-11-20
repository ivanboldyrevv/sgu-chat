import os

from flask import redirect, url_for, request

from werkzeug.utils import secure_filename

from website.repo.repository import RepositoryFactory


class PostActivity:
    def __init__(self, user_id):
        self.IMAGE_EXTENSIONS = {'png', 'jpeg', 'jpg'}
        self.VIDEO_EXTENSIONS = {'mp4', 'mov', 'wmv', 'webm'}
        self.UPLOAD_PATH = 'website/static/post_files'

        self.user_id = user_id

        self.repository = RepositoryFactory()

        self.like_repository = self.repository.create_likes_repository()
        self.stats_repository = self.repository.create_statistics_repository()
        self.bookmark_repository = self.repository.create_bookmark_repository()
        self.post_repository = self.repository.create_post_repository()

        self.action_dict = {
            'like': self.like_or_unlike,
            'open-comments': self.redirect_to_comments,
            'bookmark': self.add_or_delete_bookmark,
            'subscribe': self.subscribe,
            'unsubscribe': self.unsubscribe,
            'new-post': self.create_new_post
        }

    # TODO: Flask - KeyError
    def action(self):
        for action in request.form:
            if action not in self.action_dict:
                continue
            return self.action_dict[action]()

    def redirect_to_comments(self):
        return redirect(url_for('post.post_page', post_id=request.form['open-comments']))

    def like_or_unlike(self):
        post_id = request.form['like']
        if self.like_repository.check_like(post_id, self.user_id):
            self.like_repository.remove_like(post_id, self.user_id)
            self.stats_repository.update_likes(post_id)
        else:
            self.like_repository.add_like(post_id, self.user_id)
            self.stats_repository.update_likes(post_id)

    def add_or_delete_bookmark(self):
        post_id = request.form['bookmark']
        if self.bookmark_repository.check_bookmark(self.user_id, post_id):
            self.bookmark_repository.remove_bookmark(self.user_id, post_id)
        else:
            self.bookmark_repository.add_bookmark(self.user_id, post_id)

    def subscribe(self):
        subscribe_id = request.form['subscribe']
        self.post_repository.subscribe(self.user_id, subscribe_id)

    def unsubscribe(self):
        subscribe_id = request.form['unsubscribe']
        self.post_repository.unsubscribe(self.user_id, subscribe_id)

    def create_new_post(self):
        title = request.form['title']
        data = request.form['data']
        author = self.user_id
        files = request.files.getlist('files')
        self.post_repository.post_to_db(title, data, author)
        for file in files:
            filetype = file.filename.rsplit('.')[1]
            filename = secure_filename(file.filename)
            if filetype in self.IMAGE_EXTENSIONS:
                filetype = 'image'
            if filetype in self.VIDEO_EXTENSIONS:
                filetype = 'video'
            file.save(os.path.join(self.UPLOAD_PATH, filename))
            self.post_repository.files_to_db(filename, filetype)

    def get_post_button_status(self, posts):
        post_statistics = {
            'like_button_status': {},
            'bookmark_button_status': {},
            'subscribe_button_status': {}
        }
        for post in posts:
            post_id = post['id']
            post_statistics['like_button_status'][post_id] = self.like_repository.check_like(post_id, self.user_id)
            post_statistics['bookmark_button_status'][post_id] = self.bookmark_repository.check_bookmark(self.user_id,
                                                                                                         post_id)
            post_statistics['subscribe_button_status'][post_id] = self.post_repository.check_sub(self.user_id,
                                                                                                 post['author_id'])

        return post_statistics

from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
from website.repo.repository import RepositoryFactory
from website.repo.actions import post_actions

home = Blueprint('home', __name__)
IMAGE_EXTENSIONS = {'png', 'jpeg', 'jpg'}
VIDEO_EXTENSIONS = {'mp4', 'mov', 'wmv', 'webm'}
UPLOAD_PATH = 'website/static/post_files'


@home.route('/', methods=['GET', 'POST'])
def home_page():
    # репозитории бд
    repository = RepositoryFactory()
    post_repo = repository.create_post_repository()
    bookmark_repo = repository.create_bookmark_repository()
    like_repo = repository.create_likes_repository()

    # id пользователя в сессии
    user_id = session.get('user_id')

    if request.method == 'POST':
        # После заполнения полей модального окна записывает данные в БД
        if 'new-post' in request.form:
            title = request.form['title']
            data = request.form['data']
            author = session.get('user_id')
            files = request.files.getlist('files')
            post_repo.post_to_db(title, data, author)
            for file in files:
                filetype = file.filename.rsplit('.')[1]
                filename = secure_filename(file.filename)
                if filetype in IMAGE_EXTENSIONS:
                    filetype = 'image'
                if filetype in VIDEO_EXTENSIONS:
                    filetype = 'video'
                file.save(os.path.join(UPLOAD_PATH, filename))
                post_repo.files_to_db(filename, filetype)
        # открытие комментов
        post_actions(bookmark_repo, like_repo, user_id)

    # рендер постов
    posts = post_repo.get_posts()

    # статус кнопок
    bookmark_status = {}
    likes_status = {}
    for post in posts:
        bookmark_status[post['id']] = bookmark_repo.check_bookmark(user_id, post['id'])
        likes_status[post['id']] = like_repo.check_like(post['id'], user_id)

    return render_template('blog/home.html', posts=posts, bookmark_status=bookmark_status, likes_status=likes_status)

from flask import Blueprint, render_template, request, session
from werkzeug.utils import secure_filename
import os
from website.auth import login_required
from website.helpers.render_posts import post_to_db, files_to_db, get_posts

home = Blueprint('home', __name__)
IMAGE_EXTENSIONS = {'png', 'jpeg', 'jpg'}
VIDEO_EXTENSIONS = {'mp4', 'mov', 'wmv', 'webm'}
UPLOAD_PATH = 'website/static/post_files'


@home.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        # После заполнения полей модального окна записывает данные в БД
        if 'new-post' in request.form:
            title = request.form['title']
            data = request.form['data']
            author = session.get('user_id')
            files = request.files.getlist('files')
            post_to_db(title, data, author)
            for file in files:
                filetype = file.filename.rsplit('.')[1]
                filename = secure_filename(file.filename)
                if filetype in IMAGE_EXTENSIONS:
                    filetype = 'image'
                if filetype in VIDEO_EXTENSIONS:
                    filetype = 'video'
                file.save(os.path.join(UPLOAD_PATH, filename))
                files_to_db(filename, filetype)

    # рендер постов
    posts = get_posts()

    return render_template('blog/home.html', posts=posts)

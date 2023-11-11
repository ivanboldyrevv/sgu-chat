import os
from flask import request
from website.db import get_db
from werkzeug.utils import secure_filename

AVATAR_PATH = 'website/static/users_files'


def change_settings(user_id):
    db = get_db()
    file = request.files['user-avatar']
    filename = secure_filename(file.filename)
    file.save(os.path.join(AVATAR_PATH, filename))
    db.execute('UPDATE user SET avatar = ? WHERE id = ?', (filename, user_id))
    db.commit()


def render_profile(user_id):
    db = get_db()
    return db.execute('SELECT * FROM user WHERE user.id = ? ', (user_id,)).fetchone()


def user_posts(user_id):
    db = get_db()
    result = db.execute('SELECT * FROM post WHERE author_id = ? ORDER BY created DESC ', (user_id,)).fetchall()
    return result

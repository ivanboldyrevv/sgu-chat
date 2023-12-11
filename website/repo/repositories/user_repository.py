from werkzeug.utils import secure_filename
from flask import request
import os


class UserRepository:
    def __init__(self, db):
        self.db = db
        self.path = 'website/static/users_files'

    def change_settings(self, user_id):
        file = request.files['user-avatar']
        filename = secure_filename(file.filename)
        file.save(os.path.join(self.path, filename))
        gender = request.form['gender']
        country = request.form['country']
        birthday = request.form['birthday']
        bio = request.form['bio']
        study = request.form['study']
        self.db.execute('UPDATE user SET avatar = ?, country = ?, birthday = ?, gender = ?, bio = ?, study = ? '
                        'WHERE id = ?',
                        (filename, country, birthday, gender, bio, study, user_id))
        self.db.commit()

    def render_profile(self, username):
        return self.db.execute('SELECT * FROM user '
                               'JOIN countries ON user.id = countries.id '
                               'WHERE username = ?', (username,)).fetchone()

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

    def get_countries(self):
        return self.db.execute('SELECT * FROM countries').fetchall()

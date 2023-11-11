from website.db import get_db


def post_to_db(title, data, author):
    db = get_db()
    db.execute('INSERT INTO post (title, data, author_id) VALUES (?, ?, ?)', (title, data, author))
    db.commit()


def files_to_db(filename, file_type):
    db = get_db()
    post_id = db.execute('SELECT id FROM post ORDER BY created DESC').fetchone()['id']
    db.execute('INSERT INTO files_post (filename, filetype, post_id) VALUES (?, ?, ?)',
               (filename, file_type, post_id), )
    db.commit()


def get_posts():
    db = get_db()
    result = db.execute('SELECT post.*, user.*, GROUP_CONCAT(files_post.filename) AS filenames '
                        'FROM post '
                        'JOIN user ON post.author_id = user.id '
                        'JOIN files_post ON post.id = files_post.post_id '
                        'GROUP BY post.id '
                        'ORDER BY post.created DESC').fetchall()
    return result


def get_post(post_id):
    db = get_db()
    result = db.execute('SELECT post.*, user.*, GROUP_CONCAT(files_post.filename) AS filenames '
                        'FROM post '
                        'JOIN user ON post.author_id = user.id '
                        'JOIN files_post ON post.id = files_post.post_id '
                        'WHERE post.id = ?', (post_id,)).fetchone()
    return result

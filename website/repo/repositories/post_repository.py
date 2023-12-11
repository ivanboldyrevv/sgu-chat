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
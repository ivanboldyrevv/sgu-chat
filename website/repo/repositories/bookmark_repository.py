class BookmarkRepository:
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
        return self.db.execute('SELECT post.*, posts_statistics.* FROM bookmarks '
                               'JOIN (SELECT post.*, user.*, GROUP_CONCAT(files_post.filename) AS filenames '
                               'FROM post '
                               'JOIN user ON post.author_id = user.id '
                               'JOIN files_post ON post.id = files_post.post_id '
                               'GROUP BY post.id ) AS post ON bookmarks.post_id = post.id '
                               'JOIN posts_statistics ON post.id = posts_statistics.post_id '
                               'WHERE bookmarks.user_id = ?', (user_id,)).fetchall()

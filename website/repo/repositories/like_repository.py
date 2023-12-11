class LikeRepository:
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

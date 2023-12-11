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
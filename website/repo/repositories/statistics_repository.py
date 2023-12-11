class StatisticsRepository:
    def __init__(self, db):
        self.db = db

    def update_views(self, post_id, views):
        self.db.execute('UPDATE posts_statistics SET views = ? WHERE post_id = ?', (views, post_id))
        self.db.commit()

    def update_likes(self, post_id):
        self.db.execute('UPDATE posts_statistics '
                        'SET likes = (SELECT COUNT(*) FROM likes WHERE post_id = ?) '
                        'WHERE post_id = ?', (post_id, post_id))
        self.db.commit()

    def get_view(self, post_id):
        return self.db.execute('SELECT views FROM posts_statistics WHERE post_id = ?', (post_id,)).fetchone()[0]
class ChatRepository:
    def __init__(self, db):
        self.db = db

    def create_group(self, friend_1, friend_2):
        self.db.execute('INSERT INTO groups (name) VALUES (?)', ('friends',))
        group_id = self.db.execute('SELECT id FROM groups ORDER BY create_date DESC').fetchone()[0]
        self.db.execute('INSERT INTO user_group (user_id, group_id) VALUES (?, ?), (?, ?)',
                        (friend_1, group_id, friend_2, group_id))
        self.db.commit()

    def message_to_db(self, user_id, group_id, message):
        self.db.execute(
            'INSERT INTO messages (data, creator_id) VALUES (?, ?)',
            (message, user_id))

        self.db.execute(
            'INSERT INTO message_recipient (recipient_id, recipient_group_id, message_id) '
            'VALUES (?, ?, (SELECT id FROM messages ORDER BY create_date DESC LIMIT 1))',
            (user_id, group_id))

        self.db.commit()

    def get_messages(self, group_id):
        return self.db.execute('SELECT * FROM message_recipient '
                               'JOIN messages ON message_recipient.message_id = messages.id '
                               'JOIN user ON message_recipient.recipient_id = user.id '
                               'WHERE recipient_group_id = ? '
                               'ORDER BY create_date ASC', (group_id,)).fetchall()

    def return_to_chat_from_friendlist(self, first, second):
        return self.db.execute('SELECT groups.id '
                               'FROM groups '
                               'JOIN user_group ON groups.id = user_group.group_id '
                               'WHERE user_id IN (?, ?) '
                               'GROUP BY groups.id '
                               'HAVING COUNT(DISTINCT user_id) = 2', (first, second)).fetchone()[0]

    def show_last_message(self, group_id):
        return self.db.execute('SELECT data, username FROM message_recipient '
                               'JOIN messages ON message_recipient.message_id = messages.id '
                               'JOIN user ON messages.creator_id = user.id '
                               'WHERE recipient_group_id = ? '
                               'ORDER BY messages.create_date DESC', (group_id,)).fetchone()

    def add_to_chat(self, user_id, group_id):
        self.db.execute('INSERT INTO user_group (user_id, group_id) VALUES (?, ?)', (user_id, group_id))
        message = (f"Пользователь {self.db.execute('SELECT username FROM user WHERE id = ?', (user_id,)).fetchone()[0]} "
                   f"был добавлен в чат")
        self.message_to_db(0, group_id, message)
        self.db.commit()

    def get_groups(self, user_id):
        return self.db.execute('SELECT * FROM groups '
                               'JOIN user_group ON groups.id = user_group.group_id '
                               'WHERE user_id = ? '
                               'ORDER BY create_date DESC', (user_id,)).fetchall()

    def change_name(self, name, group_id):
        self.db.execute('UPDATE groups SET name = ? WHERE id = ?', (name, group_id))
        self.db.commit()

    def change_avatar(self, filename, group_id):
        self.db.execute('UPDATE groups SET group_avatar = ? WHERE id = ?', (filename, group_id))
        self.db.commit()

    def show_users_in_chat(self, user_id, group_id):
        return self.db.execute('SELECT id FROM user_group WHERE user_id = ? AND group_id = ?',
                               (user_id, group_id)).fetchall()

    def delete_user_from_chat(self, user_id, group_id):
        message = (f"Пользователь {self.db.execute('SELECT username FROM user WHERE id = ?',(user_id,)).fetchone()[0]}"
                   f" был удален из чата")
        self.db.execute('DELETE FROM user_group WHERE user_id = ? AND group_id = ?', (user_id, group_id))
        self.message_to_db(0, group_id, message)
        self.db.commit()

from flask import redirect, url_for, request

from website.repo.repository import RepositoryFactory


class ChatActivity:
    def __init__(self, user_id, room_id):
        self.room_id = room_id
        self.user_id = user_id

        self.repository = RepositoryFactory()
        self.chat_repository = self.repository.create_chat_repository()

        self.messages = self.chat_repository.get_messages(room_id)

        self.activity_dict = {
            'send-message': self.send_message,
            'to-chat': self.create_chat
        }

    def actions(self):
        for action in request.form:
            if action not in self.activity_dict:
                continue
            return self.activity_dict[action]()

    def create_chat(self):
        to_user = request.form['to-chat']
        self.chat_repository.create_group(self.user_id, to_user)
        return redirect(url_for('chat.chats'))

    def send_message(self):
        message_data = request.form['message-data']
        self.chat_repository.message_to_db(self.user_id, self.room_id, message_data)
        return redirect(url_for('chat.chats', id=self.room_id))

    def last_messages(self, groups):
        last_message = {}
        for group in groups:
            last_message[group['group_id']] = self.chat_repository.show_last_message(group['group_id'])
        return last_message

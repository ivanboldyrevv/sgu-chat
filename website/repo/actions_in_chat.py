from flask import redirect, url_for, request

import os

from website.repo.repository_factory import RepositoryFactory


class ChatActivity:
    def __init__(self, user_id, room_id):
        self.room_id = room_id
        self.user_id = user_id

        self.UPLOAD_PATH = 'website/static/chat_files'

        self.repository = RepositoryFactory()
        self.chat_repository = self.repository.create_chat_repository()

        self.messages = self.chat_repository.get_messages(self.room_id)

        self.activity_dict = {
            'send-message': self.send_message,
            'to-chat': self.create_chat,
            'add-to-chat': self.add_new_chatter,
            'chat-settings': self.chat_settings,
            'delete-from-chat': self.delete_user
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
            message = self.chat_repository.show_last_message(group['group_id'])
            last_message[group['group_id']] = message
        return last_message

    def show_messages(self):
        return self.chat_repository.get_messages(self.room_id)

    def add_new_chatter(self):
        new_chatter = request.form['add-to-chat']
        self.chat_repository.add_to_chat(new_chatter, self.room_id)
        return redirect(url_for('chat.chats', id=self.room_id))

    def chat_settings(self):
        self.change_group_avatar()
        self.change_group_name()

    def change_group_name(self):
        new_name = request.form['chat-name']
        self.chat_repository.change_name(new_name, self.room_id)

    def change_group_avatar(self):
        file = request.files['chat-pic']
        filename = file.filename
        file.save(os.path.join(self.UPLOAD_PATH, filename))
        self.chat_repository.change_avatar(filename, self.room_id)

    def users_in_chat(self, friends):
        users = {}
        for friend in friends:
            boolean = True if self.chat_repository.show_users_in_chat(friend['user_id'], self.room_id) else False
            users[friend['user_id']] = boolean
        return users

    def delete_user(self):
        delete_id = request.form['delete-from-chat']
        self.chat_repository.delete_user_from_chat(delete_id, self.room_id)
        return redirect(url_for('chat.chats', id=self.room_id))

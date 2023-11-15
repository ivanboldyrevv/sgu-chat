"""Страница чата"""
from flask import Blueprint, render_template, session, request
from website.repo.repository import RepositoryFactory
from website.repo.actions import chat_actions

chat = Blueprint('chat', __name__)


@chat.route('/chat', methods=['GET', 'POST'])
def chats():
    # id юзера
    user_id = session.get('user_id')
    # arg url
    arg = request.args.get('id')
    # открываем репозиторий чата и добавляем контакты из репозитория юзера
    repository = RepositoryFactory()
    user_repo = repository.create_user_repository()
    friends = user_repo.get_friends(user_id)
    # репозиторий чата
    chat_repo = repository.create_chat_repository()
    groups = chat_repo.get_groups(user_id)
    # сообщения в диалоге
    messages = repository.create_chat_repository().get_messages(request.args.get('id'))

    if request.method == 'POST':
        chat_actions(user_id, arg, chat_repo)

    # переадрессация на страницу диалога
    if request.args.get('id'):
        return render_template('chat/dialog.html', messages=messages)

    return render_template('chat/chat.html', friends=friends, groups=groups)

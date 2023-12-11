from flask import Blueprint, render_template, session, request, redirect, url_for
from website.repo.repository_factory import RepositoryFactory
from website.repo.actions_in_chat import ChatActivity

chat = Blueprint('chat', __name__)


@chat.route('/chat', methods=['GET', 'POST'])
def chats():
    user_id = session.get('user_id')
    room_id = request.args.get('id')

    repository = RepositoryFactory()
    chat_repo = repository.create_chat_repository()
    user_repo = repository.create_user_repository()

    activity = ChatActivity(user_id, room_id)

    # Данные для главной страницы чата
    friends = user_repo.get_friends(user_id)
    groups = chat_repo.get_groups(user_id)
    last_message = activity.last_messages(groups)

    # Данные для диалога
    messages = chat_repo.get_messages(room_id)
    check_users_in_chat = activity.users_in_chat(friends)

    if request.method == 'POST':
        actions = ChatActivity(user_id, room_id).actions()
        if actions:
            return actions

    # переадрессация на страницу диалога
    if room_id:
        return render_template('chat/dialog.html', friends=friends, messages=messages,
                               check_users_in_chat=check_users_in_chat)

    return render_template('chat/chat.html', friends=friends, groups=groups, last_message=last_message)

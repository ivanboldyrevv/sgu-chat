from flask import Blueprint, render_template, session, request
from website.repo.repository import RepositoryFactory
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
    messages = activity.messages

    if request.method == 'POST':
        activity.actions()
        if activity:
            return activity

    # переадрессация на страницу диалога
    if room_id:
        return render_template('chat/dialog.html', messages=messages)

    return render_template('chat/chat.html', friends=friends, groups=groups, last_message=last_message)

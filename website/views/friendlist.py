from flask import Blueprint, render_template, request, redirect, url_for
from website.repo.repository_factory import RepositoryFactory

friends = Blueprint('friends', __name__)


@friends.route('/friends', methods=['GET', 'POST'])
def friendlist():
    repository = RepositoryFactory()
    friends_data = repository.create_user_repository()
    arg = int(request.args.get('id'))
    if request.method == 'POST':
        if 'accept-friend' in request.form:
            friends_data.update_status('friendship', request.form['accept-friend'], arg)
        if 'to-chat' in request.form:
            ids = repository.create_chat_repository().return_to_chat_from_friendlist(arg, request.form['to-chat'])
            return redirect(url_for('chat.chats', id=ids))

    friend_request = friends_data.check_request('get', arg)

    friendlist_data = friends_data.get_friends(arg)

    return render_template('profile/friends.html', arg=arg, friend_request=friend_request, friendlist=friendlist_data)

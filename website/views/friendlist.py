from flask import Blueprint, render_template, request, session
from website.repo.repository import RepositoryFactory

friends = Blueprint('friends', __name__)


@friends.route('/friends', methods=['GET', 'POST'])
def friendlist():
    repository = RepositoryFactory()
    friends_data = repository.create_user_repository()
    arg = int(request.args.get('id'))
    if request.method == 'POST':
        if 'accept-friend' in request.form:
            friends_data.update_status('friendship', request.form['accept-friend'], arg)

    friend_request = friends_data.check_request('get', arg)

    friendlist_data = friends_data.get_friends(arg)

    return render_template('profile/friends.html', arg=arg, friend_request=friend_request, friendlist=friendlist_data)

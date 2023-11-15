from flask import Blueprint, render_template, request, session
from website.repo.repository import RepositoryFactory

profile = Blueprint('profile', __name__, url_prefix='/u')


@profile.route('/<username>', methods=['GET', 'POST'])
def profile_page(username):
    repository = RepositoryFactory()
    user_repo = repository.create_user_repository()
    user_id = session.get('user_id')
    arg = request.args.get('id')
    if request.method == 'POST':
        # изменение настроик пользователя
        if 'change-settings' in request.form:
            user_repo.change_settings(user_id)
        if 'call-request' in request.form:
            user_repo.call_request(user_id, request.form['call-request'])
        if 'recall-request' in request.form:
            user_repo.recall_request(user_id, request.form['recall-request'])

    # рендер страницы профиля
    user_profile = user_repo.render_profile(username)
    posts = user_repo.user_posts(user_id)
    check_request = user_repo.check_request('recall', user_id, arg)

    return render_template('profile/profile.html', profile=user_profile, posts=posts, check_request=check_request)



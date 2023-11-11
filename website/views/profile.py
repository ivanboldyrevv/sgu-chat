from flask import Blueprint, render_template, request, session
from website.helpers.user_settings import change_settings, render_profile, user_posts

profile = Blueprint('profile', __name__, url_prefix='/u')


@profile.route('/<username>', methods=['GET', 'POST'])
def profile_page(username):
    user_id = session.get('user_id')
    if request.method == 'POST':
        # изменение настроик пользователя
        if 'change-settings' in request.form:
            change_settings(user_id)

    # рендер страницы профиля
    user_profile = render_profile(user_id)
    posts = user_posts(user_id)

    return render_template('profile/profile.html', profile=user_profile, posts=posts)

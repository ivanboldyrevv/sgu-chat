from flask import Blueprint, render_template, request, session, redirect, url_for

from werkzeug.utils import secure_filename

import os

from website.repo.repository import RepositoryFactory

from website.repo.actions_in_post import PostActivity

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def home_page():
    user_id = session.get('user_id')

    repository = RepositoryFactory()
    post_repository = repository.create_post_repository()
    posts = post_repository.get_posts()

    activity = PostActivity(user_id)

    if request.method == 'POST':
        actions = activity.action()
        if actions:
            return actions

    button_status = activity.get_post_button_status(posts)

    return render_template('blog/home.html', posts=posts, button_status=button_status)

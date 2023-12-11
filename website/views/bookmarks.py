from flask import Blueprint, render_template, session, request

from website.repo.repository_factory import RepositoryFactory
from website.repo.actions_in_post import PostActivity

bookmark = Blueprint('bookmarks', __name__)


@bookmark.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    # репозитории бд
    repository = RepositoryFactory()
    bookmark_repository = repository.create_bookmark_repository()

    user_id = session.get('user_id')

    bookmark_activity = PostActivity(user_id)

    if request.method == 'POST':
        actions = bookmark_activity.action()
        if actions:
            return actions

    # данные для закладок
    posts = bookmark_repository.get_bookmarks(user_id)
    button_status = bookmark_activity.get_post_button_status(posts)

    return render_template('blog/bookmarks.html', posts=posts, button_status=button_status)

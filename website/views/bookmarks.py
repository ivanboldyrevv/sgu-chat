from flask import Blueprint, render_template, session, request

from website.repo.repository import RepositoryFactory


bookmark = Blueprint('bookmarks', __name__)


@bookmark.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    # репозитории бд
    repository = RepositoryFactory()

    bookmark_repo = repository.create_bookmark_repository()
    like_repo = repository.create_likes_repository()
    stats_repo = repository.create_statistics_repository()
    post_repo = repository.create_post_repository()

    user_id = session.get('user_id')

    if request.method == 'POST':
        pass

    # данные для закладок
    posts = bookmark_repo.get_bookmarks(user_id)

    # статус кнопок
    bookmark_status = {}
    likes_status = {}
    for post in posts:
        bookmark_status[post['id']] = bookmark_repo.check_bookmark(user_id, post['id'])
        likes_status[post['id']] = like_repo.check_like(post['id'], user_id)

    return render_template('blog/bookmarks.html', posts=posts, bookmark_status=bookmark_status,
                           likes_status=likes_status)

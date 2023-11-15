from flask import Blueprint, render_template, request, session
from website.repo.repository import RepositoryFactory

post = Blueprint('post', __name__, url_prefix='/post')


@post.route('/<post_id>', methods=['GET', 'POST'])
def post_page(post_id):
    repository = RepositoryFactory()
    post_repo = repository.create_post_repository()
    comment_repo = repository.create_comments_repository()
    statistics_repo = repository.create_statistics_repository()
    user_id = session.get('user_id')
    if request.method == 'GET':
        view = int(statistics_repo.get_view(post_id))
        view += 1
        statistics_repo.update_views(post_id, view)
    if request.method == 'POST':
        if 'submit-comment' in request.form:
            data = request.form['comment']
            comment_repo.comment_to_db(data, post_id, user_id)
    # данные для страницы с постом
    post_on_page = post_repo.get_post(post_id)
    comments_on_page = comment_repo.get_comments(post_id)

    return render_template('blog/post.html', post=post_on_page, comments=comments_on_page)

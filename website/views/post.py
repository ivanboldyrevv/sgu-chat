from flask import Blueprint, render_template
from website.helpers.render_posts import get_post

post = Blueprint('post', __name__, url_prefix='/post')


@post.route('/<post_id>', methods=['GET', 'POST'])
def post_page(post_id):
    post_on_page = get_post(post_id)
    return render_template('blog/post.html', post=post_on_page)

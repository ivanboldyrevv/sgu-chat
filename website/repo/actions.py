from flask import request, redirect, url_for

"""Действия при пост запросах на главной странице и странице поста"""


def post_actions(bookmark_repo, like_repo, user_id):
    if 'open-comments' in request.form:
        open_comments()
    if 'like' in request.form:
        like(like_repo, user_id)
    if 'bookmark' in request.form:
        bookmark(bookmark_repo, user_id)


def open_comments():
    return redirect(url_for('post.post_page', post_id=request.form['open-comments']))


def like(like_repo, user_id):
    post_id = request.form['like']
    if like_repo.check_like(post_id, user_id):
        like_repo.remove_like(post_id, user_id)
    else:
        like_repo.add_like(post_id, user_id)


def bookmark(bookmark_repo, user_id):
    post_id = request.form['bookmark']
    if bookmark_repo.check_bookmark(user_id, post_id):
        bookmark_repo.remove_bookmark(user_id, post_id)
    else:
        bookmark_repo.add_bookmark(user_id, post_id)


"""Действия при пост запросах чата"""


def chat_actions(user_id, arg, chat_repo):
    if 'open-chat' in request.form:
        friend_id = request.form['open-chat']
        chat_repo.add_group(user_id, friend_id)
        return redirect(url_for('chat.chats'))
    if 'send-message' in request.form:
        send_message(user_id, chat_repo, arg)


def send_message(user_id, chat_repo, arg):
    message_data = request.form['message-data']
    chat_repo.message_to_db(user_id, arg, message_data)
    return redirect(url_for('chat.chats', id=arg))


DROP TABLE user;
DROP TABLE post;
DROP TABLE files_post;
DROP TABLE comments;
DROP TABLE posts_statistics;
DROP TABLE bookmarks;
DROP TABLE friendlist;
DROP TABLE groups;
DROP TABLE user_group;
DROP TABLE message_recipient;
DROP TABLE messages;
DROP TABLE role;
DROP TABLE subscribers;


CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(32) UNIQUE NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    avatar TEXT NULL,
    country TEXT NULL,
    birthday TEXT NULL,
    gender TEXT NULL,
    bio TEXT NULL,
    study TEXT NULL
);

INSERT INTO user (id, username, email, password) VALUES (0, 'system', 'system@system.sys', 'asd');

CREATE TABLE IF NOT EXISTS post(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    data TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER NOT NULL,
    FOREIGN KEY(author_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS files_post(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    filetype TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    post_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES post(id)
);

CREATE TABLE IF NOT EXISTS comments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    post_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES post(id),
    FOREIGN KEY(author_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS posts_statistics(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    views INTEGER NULL,
    likes INTEGER NULL,
    reposts INTEGER NULL,
    post_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES post(id)
);

CREATE TABLE IF NOT EXISTS bookmarks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES post(id),
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS likes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES post(id),
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS friendlist(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL,
    friend_1 INTEGER NOT NULL,
    friend_2 INTEGER NOT NULL,
    FOREIGN KEY(friend_1) REFERENCES user(id),
    FOREIGN KEY(friend_2) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS groups(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    group_avatar TEXT NULL,
    create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_group(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(group_id) REFERENCES groups(id)
);

CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    creator_id INTEGER NOT NULL,
    FOREIGN KEY(creator_id) REFERENCES message_recipient(recipient_id)
);

CREATE TABLE IF NOT EXISTS message_recipient(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_id INTEGER NOT NULL,
    recipient_group_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    is_read NULL,
    FOREIGN KEY(recipient_id) REFERENCES user(id),
    FOREIGN KEY(recipient_group_id) REFERENCES groups(id),
    FOREIGN KEY(message_id) REFERENCES messages(id)
);

CREATE TABLE IF NOT EXISTS role(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_role TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS subscribers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subscription INTEGER NOT NULL,
    create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(subscription) REFERENCES user(id)
);


CREATE TABLE IF NOT EXISTS countries(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);
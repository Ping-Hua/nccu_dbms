PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS reply;
DROP TABLE IF EXISTS review;

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    student_number INTEGER, -- not null
    phone INTEGER, -- not null
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE post (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_user_id INTEGER, -- fk
    book_id INTEGER, -- fk
    book_condition TEXT, -- not null
    price INTEGER, -- not null
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE book (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name  TEXT NOT NULL,
    ISBN TEXT ,--NOT NULL UNIQUE, -- ISBN 不可重複且必填
    author TEXT NOT NULL, -- 作者必填
    version TEXT, -- not null
    public_year INTEGER ,-- not null
    publisher TEXT, --not null
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP -- 自動生成建立時間
);

CREATE TABLE genre (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT, -- not null
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reply (
    reply_id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_user_id INTEGER, -- fk
    to_user_id INTEGER, -- fk
    post_id INTEGER, -- fk
    message TEXT, -- not null
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE review (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_user_id INTEGER, -- fk
    to_user_id INTEGER, -- fk
    content TEXT, -- not null
    score INTEGER, -- not null
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);
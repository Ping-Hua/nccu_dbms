'''
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE book_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    book_condition TEXT,
    price INTEGER NOT NULL,
    post_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    seller_id INTEGER,                     -- 賣家 ID
    isbn INTEGER                        -- 書籍 ISBN

    -- 外鍵約束
   -- FOREIGN KEY (seller_id) REFERENCES sellers (id),
   -- FOREIGN KEY (isbn) REFERENCES books (isbn)
);
'''
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
    ISBN INTEGER, -- pk?
    book_name TEXT, -- not null
    author TEXT, --not null
    version TEXT, -- not null
    public_year YEAR, -- not null
    publisher TEXT, --not null
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
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
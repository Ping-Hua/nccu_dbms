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

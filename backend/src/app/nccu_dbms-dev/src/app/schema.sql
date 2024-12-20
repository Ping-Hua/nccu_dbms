DROP TABLE IF EXISTS user;
CREATE TABLE user (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS post;
CREATE TABLE post (
    PostID INTEGER PRIMARY KEY AUTOINCREMENT,
    SellerID INT NOT NULL,
    ISBN INT,
    BookPrice INT NOT NULL,
    BookCondition TEXT NOT NULL,
    PostTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,      
    FOREIGN KEY (SellerID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN) ON DELETE SET NULL
);





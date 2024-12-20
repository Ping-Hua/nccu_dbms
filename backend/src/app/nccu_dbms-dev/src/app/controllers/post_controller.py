from flask import jsonify, request, g
import logging
from sqlite3 import IntegrityError
from app.database import get_db

class PostController:
    def add_post(self):
        logging.info("----- PostController.add_post -----")
        try:
            user_id = g.user_id  # 從登入狀態取得 UserID
            if not user_id:
                return jsonify({"error": "User not authenticated"}), 401

            data = request.get_json()
            isbn = data.get('ISBN') # Book Table
            book_name = data.get('BookName') # Book Table
            price = data.get('Price')
            book_condition = data.get('BookCondition')
            content = data.get('content')

            if not isbn or not book_name or not price or not book_condition or not content:
                return jsonify({
                    "error": "ISBN, BookName, Price, BookCondition, and content are required fields"
                }), 400

            db = get_db()
            cursor = db.cursor()

            cursor.execute("SELECT BookID FROM Book WHERE ISBN = ?", (isbn,))
            book = cursor.fetchone()

            if book:
                book_id = book[0]  # 已存在的 BookID
            else:
                # 若 ISBN 不存在，新增書籍並取得 BookID
                cursor.execute(
                    "INSERT INTO Book (ISBN, BookName) VALUES (?, ?)",
                    (isbn, book_name)
                )
                db.commit()
                book_id = cursor.lastrowid

            # 插入貼文資料
            cursor.execute(
                """
                INSERT INTO post (UserID, BookID, Price, BookCondition, content)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, book_id, price, book_condition, content)
            )
            db.commit()

            post_id = cursor.lastrowid
            return jsonify({
                "message": "Post added successfully",
                "PostID": post_id,
                "BookID": book_id
            }), 201

        except IntegrityError as e:
            logging.error(f"Database error: {e}")
            return jsonify({"error": "Integrity error, possibly duplicate ISBN"}), 400

        except Exception as e:
            logging.error(f"Error adding post: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

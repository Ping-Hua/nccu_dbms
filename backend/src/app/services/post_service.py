from app.database import use_db
import logging

class PostService:
    @staticmethod
    @use_db
    def add_post(cursor, seller_user_id, book_id, book_condition, price):
        logging.info('info', 'add_post called with parameters: seller_user_id={seller_user_id}, book_id={book_id}, book_condition={book_condition}, price={price}')

        # 插入資料
        cursor.execute(
            "INSERT INTO post (seller_user_id, book_id, book_condition, price) VALUES (?,?,?,?)", 
            (seller_user_id, book_id, book_condition, price)
        )

        post_id = cursor.lastrowid
        logging.info(f"Post added successfully: {post_id}")

        post_data = {
            "post_id": post_id,
            "seller_user_id": seller_user_id,
            "book_id": book_id,
            "book_condition": book_condition,
            "price": price,
        }
        return post_data
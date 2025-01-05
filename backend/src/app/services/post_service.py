from app.database import use_db,get_db
import logging
import json

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
    
    @use_db
    def update_post_book(cursor, post_id, book_id):
        cursor.execute(
            "UPDATE post SET book_id = ? WHERE post_id = ?",
            (book_id, post_id)
        )

        logging.info(f"Post's book update successfully: {post_id}")
        cursor.execute(
            "SELECT post_id, book_id "
            "FROM post WHERE post_id = ?", 
            (post_id,)
        )

        post_data = {
            "book_id": book_id,
        }

        return post_data
        
    @use_db
    def update_post_book_condition(cursor, post_id, book_condition):
        cursor.execute(
            "UPDATE post SET book_condition = ? WHERE post_id = ?",
            (book_condition, post_id)
        )

        logging.info(f"Post's book condition update successfully: {post_id}")

        post_data = {
            "book_condition": book_condition,
        }

        return post_data
    
    @use_db
    def update_post_price(cursor, post_id, price):
        
        cursor.execute(
            "UPDATE post SET price = ? WHERE post_id = ?",
            (price, post_id)
        )

        logging.info(f"Post's price update successfully: {post_id}")

        post_data = {
            "price": price,
        }

        return post_data
        
    @staticmethod
    @use_db
    def get_post(cursor, post_id):

        cursor.execute(
            "SELECT post_id, seller_user_id, book_id, book_condition, price, create_time "
            "FROM post WHERE post_id =?", 
            (post_id,)
        )
        post = cursor.fetchone()

        post_data = {
            "post_id": post[0],
            "seller_user_id": post[1],
            "book_id": post[2],
            "book_condition": post[3],
            "price": post[4],
            "create_time": post[5]
        }
        return post_data
        
    @use_db
    def get_all_post(cursor):
        cursor.execute(
            "SELECT post_id, seller_user_id, book_id, book_condition, price, create_time FROM post"
        )
        posts = cursor.fetchall()
        post_json = []
        for post in posts:
            post_data = {
                "post_id": post[0],
                "seller_user_id": post[1],
                "book_id": post[2],
                "book_condition": post[3],
                "price": post[4],
                "create_time": post[5]
            }
            post_json.append(post_data)
        return post_json
        
    @use_db
    def get_all_post_by_book(cursor, book_id):
        cursor.execute(
            "SELECT post_id, seller_user_id, book_id, book_condition, price, create_time FROM post "
            "WHERE book_id = ?",
            (book_id,)
        )
        posts = cursor.fetchall()
        post_json = []
        for post in posts:
            post_data = {
                "post_id": post[0],
                "seller_user_id": post[1],
                "book_id": post[2],
                "book_condition": post[3],
                "price": post[4],
                "create_time": post[5]
            }
            post_json.append(post_data)
        return post_json
    def service_delete_post(post_id):
        db = get_db()
        cursor = db.cursor()

        try:
            # 查找貼文
            cursor.execute('SELECT post_id, seller_user_id FROM post WHERE post_id = ?', (post_id,))
            post = cursor.fetchone()
            if post is None:
                logging.warning(f"Post with post_id {post_id} does not exist.")
                return None  # 貼文不存在

            # 刪除貼文
            cursor.execute('DELETE FROM post WHERE post_id = ?', (post_id,))
            db.commit()

            # 回傳刪除的貼文資訊
            deleted_post = {
                "post_id": post[0],  # 第一個欄位:post id
                "seller_user_id": post[1]  # 第二個欄位:user id 
            }
            logging.info(f"Post with post_id {post_id} deleted successfully.")
            return deleted_post

        except Exception as e:
            db.rollback()
            logging.error(f"Error deleting post with post_id {post_id}: {str(e)}")
            raise e
from app.database import get_db
import logging
class PostService:
    @staticmethod
    def add_post(seller_user_id, book_id, book_condition, price):
        logging.info('info', 'add_post called with parameters: seller_user_id={seller_user_id}, book_id={book_id}, book_condition={book_condition}, price={price}')
        
        db = get_db()
        cursor = db.cursor()
        
        try:
            # 驗證 seller_user_id 存在
            #cursor.execute("SELECT 1 FROM user WHERE user_id =?", (seller_user_id,))
            #if cursor.fetchone() is None:
            #    raise ValueError(f"Seller with ID {seller_user_id} does not exist")

            # 插入資料
            cursor.execute(
                "INSERT INTO post (seller_user_id, book_id, book_condition, price) VALUES (?,?,?,?)", 
                (seller_user_id, book_id, book_condition, price)
            )
            db.commit()

            post_id = cursor.lastrowid
            logging.info(f"Post added successfully: {post_id}")

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
        
        except ValueError as e:
            logging.warning(f"Validation error: {str(e)}")
            raise e
        except Exception as e:
            db.rollback()
            logging.error(f"Database error: {str(e)}")
            raise e
    def service_delete_post(post_id):
        db = get_db()
        cursor = db.cursor()

        # 查找貼文
        cursor.execute('SELECT * FROM book_posts WHERE id = ?', (post_id,))
        post = cursor.fetchone()
        if post is None:
            return None  # 貼文不存在

        # 刪除貼文
        cursor.execute('DELETE FROM book_posts WHERE id = ?', (post_id,))
        db.commit()

         # 回傳刪除的貼文資訊
        return {"id": post["id"], "title": post["title"]}

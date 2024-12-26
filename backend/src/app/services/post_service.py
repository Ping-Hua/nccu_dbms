from app.database import get_db
import logging
import json

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

    def update_post_book(post_id, book_id):
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "UPDATE post SET book_id = ? WHERE post_id = ?",
                (book_id, post_id)
            )
            db.commit()

            logging.info(f"Post's book update successfully: {post_id}")
            cursor.execute(
                "SELECT post_id, book_id "
                "FROM post WHERE post_id = ?", 
                (post_id,)
            )
            print(789)

            post = cursor.fetchone()
            print(post)

            post_data = {
                "book_id": post[1],
            }

            return post_data
        except ValueError as e:
            logging.warning(f"Validation error: {str(e)}")
            raise e
        except Exception as e:
            db.rollback()
            logging.error(f"Database error: {str(e)}")
            raise e

    def update_post_book_condition(post_id, book_condition):
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "UPDATE post SET book_condition = ? WHERE post_id = ?",
                (book_condition, post_id)
            )
            db.commit()

            logging.info(f"Post's book condition update successfully: {post_id}")

            cursor.execute(
                "SELECT post_id, book_condition "
                "FROM post WHERE post_id =?", 
                (post_id,)
            )
            post = cursor.fetchone()

            post_data = {
                "book_condition": post[1],
            }

            return post_data
        except ValueError as e:
            logging.warning(f"Validation error: {str(e)}")
            raise e
        except Exception as e:
            db.rollback()
            logging.error(f"Database error: {str(e)}")
            raise e
    def update_post_price(post_id, price):
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "UPDATE post SET price = ? WHERE post_id = ?",
                (price, post_id)
            )
            db.commit()

            logging.info(f"Post's price update successfully: {post_id}")

            cursor.execute(
                "SELECT post_id, price "
                "FROM post WHERE post_id =?", 
                (post_id,)
            )
            post = cursor.fetchone()

            post_data = {
                "price": post[1],
            }

            return post_data
        except ValueError as e:
            logging.warning(f"Validation error: {str(e)}")
            raise e
        except Exception as e:
            db.rollback()
            logging.error(f"Database error: {str(e)}")
            raise e

    @staticmethod
    def get_post(post_id):

        db = get_db()
        cursor = db.cursor()

        try:
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
        
    def get_all_post():
        db = get_db()
        cursor = db.cursor()

        try:
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

        except ValueError as e:
            logging.warning(f"Validation error: {str(e)}")
            raise e
        except Exception as e:
            db.rollback()
            logging.error(f"Database error: {str(e)}")
            raise e
        
    def get_all_post_by_book(book_id):
        db = get_db()
        cursor = db.cursor()

        try:
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

        except ValueError as e:
            logging.warning(f"Validation error: {str(e)}")
            raise e
        except Exception as e:
            db.rollback()
            logging.error(f"Database error: {str(e)}")
            raise e
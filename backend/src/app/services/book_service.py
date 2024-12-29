from app.database import get_db
import logging

class BookService():
    def search(self,book_name):
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute('SELECT * FROM book WHERE book_name=?',book_name)
            if cursor is None:
                logging.warning(f"Book names {book_name} does not exist.")
                return None  # 貼文不存在
            else:
                logging.info(f"Books with book name {book_name} search successfully.")
                book_data = []
                for book in cursor:
                    book_data = {
                        "book_id": book[0],
                        "ISBN": book[1],
                        "author": book[2],
                        "version": book[3],
                        "public_year": book[4],
                        "publisher": book[5],
                        "create_time": book[6]
                    }
                    book_data.append(book_data)
            return book_data
        except Exception as e:
            db.rollback()
            logging.error(f"Error searching books with book name or auther {book_name}: {str(e)}")
            raise e

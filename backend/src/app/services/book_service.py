from app.database import get_db
import logging

class BookService():
    def adding_book(book_name,author):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
            "INSERT INTO book (book_name,author) VALUES (?, ?)", 
                (book_name,author)
            )
            db.commit()
            book_id = cursor.lastrowid
            logging.info(f"Book added successfully: {book_id}")

            cursor.execute(
                "SELECT * "
                "FROM book WHERE book_id = ?", book_id
            )
            book = cursor.fetchone()

            book_data = {
                    "book_id": book[0],
                    "book_name": book[1],
                    "ISBN": book[2],
                    "author": book[3],
                    "version": book[4],
                    "public_year": book[5],
                    "publisher": book[6],
                    "create_time": book[7]
                }
            return book_data
        except Exception as e:
            db.rollback()
            logging.error(f"Error adding books with book name/auther {book_name}: {str(e)}")
            raise e
            
    def search(self,bookname):
        db = get_db()
        cursor = db.cursor()
        search_book = f'%{bookname.lower()}%' # 添加通配符以支持模糊查詢
        try:
            cursor.execute('SELECT * FROM book WHERE LOWER(book_name) LIKE ? OR LOWER(author) LIKE ?',(search_book,search_book))
            results = cursor.fetchall()
            
            if not results:
                logging.warning(f"Book name/author {search_book} does not exist.")
                return None  # 不存在
            
            book_data = []
            
            for book in results:
                book_data = {
                    "book_id": book[0],
                    "book_name": book[1],
                    "ISBN": book[2],
                    "author": book[3],
                    "version": book[4],
                    "public_year": book[5],
                    "publisher": book[6],
                    "create_time": book[7]
                }
                book_data.append(book_data)
            logging.info(f"Books with query '{bookname}' retrieved successfully.")
            
            return book_data
        except Exception as e:
            db.rollback()
            logging.error(f"Error searching books with book name/auther {bookname}: {str(e)}")
            raise e
        finally:
            cursor.close()

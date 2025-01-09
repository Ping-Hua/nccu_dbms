from app.database import use_db
import logging
from app.errors.custom_exceptions import ResourceNotFoundError, ValidationError

class BookService:
    @staticmethod
    @use_db
    def adding_book(cursor, ISBN, book_name, author, version, public_year, publisher, book_picture_url):
        logging.info('info', 'adding book called with parameter: ISBN={ISBN}, book_name={book_name}, author={author}, version={version}, public_year={public_year}, publisher={publisher}')
        
        if any(v is None for v in [ISBN, book_name, author, version, public_year, publisher, book_picture_url]):
            raise ValidationError("Missing required fields: ISBN, book_name, author, version, public_year, publisher, book_picture_url")

        # 判斷 ISBN 唯一
        cursor.execute(
            "SELECT COUNT(*) FROM book WHERE ISBN = ?", (ISBN,))
        result = cursor.fetchone()

        if result[0] > 0:
            raise ValidationError(f"ISBN: {ISBN} already exists in the database.")

        cursor.execute(
            "INSERT INTO book (ISBN, book_name, author, version, public_year, publisher, book_picture_url) VALUES (?, ?, ?, ?, ?, ?, ?)", 
            (ISBN, book_name, author, version, public_year, publisher, book_picture_url)
        )

        book_id = cursor.lastrowid # 獲取新增書籍的 ID
        logging.info(f"Book added successfully: {book_id}")

        book_data = {
            "book_id": book_id,         
            "book_name": book_name,
            "ISBN": ISBN,      
            "author": author,
            "version": version,
            "public_year": public_year,
            "publisher": publisher,
            "book_picture_url": book_picture_url
        }

        return book_data
        

        
        
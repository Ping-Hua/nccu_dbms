from app.database import use_db
import logging
from app.errors.custom_exceptions import ResourceNotFoundError, ValidationError

class BookService:
    @staticmethod
    @use_db
    def adding_book(cursor, ISBN, book_name, author, public_year, publisher, book_picture_url, genre_id):
        logging.info('info', 'adding book called with parameter: ISBN={ISBN}, book_name={book_name}, author={author}, public_year={public_year}, publisher={publisher}')
        
        if any(v is None for v in [ISBN, book_name, author, public_year, publisher, book_picture_url, genre_id]):
            raise ValidationError("Missing required fields: ISBN, book_name, author, public_year, publisher, book_picture_url, genre_id")

        # 判斷 ISBN 唯一
        cursor.execute(
            "SELECT COUNT(*) FROM book WHERE ISBN = ?", (ISBN,))
        result = cursor.fetchone()

        if result[0] > 0:
            raise ValidationError(f"ISBN: {ISBN} already exists in the database.")

        cursor.execute(
            "INSERT INTO book (ISBN, book_name, author, public_year, publisher, book_picture_url, genre_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
            (ISBN, book_name, author, public_year, publisher, book_picture_url, genre_id)
        )

        book_id = cursor.lastrowid # 獲取新增書籍的 ID
        logging.info(f"Book added successfully: {book_id}")

        book_data = {
            "book_id": book_id,         
            "book_name": book_name,
            "ISBN": ISBN,      
            "author": author,
            "public_year": public_year,
            "publisher": publisher,
            "book_picture_url": book_picture_url,
            "genre_id": genre_id
        }

        return book_data
        
    @staticmethod
    @use_db
    def get_all_books(cursor):
        cursor.execute(
            "SELECT book_id, book_name, ISBN, author, public_year, book_picture_url, genre_id FROM book"
        )
        books = cursor.fetchall()
        if books is None:
            raise ResourceNotFoundError("Unable to find book list")
        book_json = []
        for book in books:
            book_data = {
                "book_id": book[0],
                "book_name": book[1],
                "ISBN": book[2],
                "author": book[3],
                "public_year": book[4],
                "book_picture_url": book[5],
                "genre_id": book[6]
            }
            book_json.append(book_data)
        return book_json
        
    @staticmethod
    @use_db
    def get_all_books_by_genre(cursor, genre_id):
        cursor.execute(
            "SELECT book_id, book_name, ISBN, author, public_year, book_picture_url, genre_id FROM book "
            "WHERE genre_id = ?",
            (genre_id,)
        )
        books = cursor.fetchall()
        if books is None:
            raise ResourceNotFoundError("Unable to find book list by genre_id")
        book_json = []
        for book in books:
            book_data = {
                "book_id": book[0],
                "book_name": book[1],
                "ISBN": book[2],
                "author": book[3],
                "public_year": book[4],
                "book_picture_url": book[5],
                "genre_id": book[6]
            }
            book_json.append(book_data)
        return book_json
        
    
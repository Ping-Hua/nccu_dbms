from app.database import use_db
import logging

class BookService:
    @staticmethod
    @use_db
    def adding_book(cursor, ISBN, book_name, author, version, public_year, publisher):
        logging.info('info', 'adding book called with parameter: ISBN={ISBN}, book_name={book_name}, author={author}, version={version}, public_year={public_year}, publisher={publisher}')
        
        cursor.execute(
            "INSERT INTO book (ISBN, book_name, author, version, public_year, publisher) VALUES (?, ?, ?, ?, ?, ?)", 
            (ISBN, book_name, author, version, public_year, publisher)
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
        }

        return book_data
        

        
        
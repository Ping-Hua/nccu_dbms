from app.database import use_db
import logging

class BookService:
    @staticmethod
    @use_db
    def adding_book(cursor, ISBN, book_name, author, version, public_year, publisher):
        logging.info('info', 'adding book called with parameter: ISBN={ISBN}, book_name={book_name}, author={author}, version={version}, public_year={public_year}, publisher={publisher}')
        
        # 判斷 ISBN 唯一
        cursor.execute(
            "SELECT COUNT(*) FROM book WHERE ISBN = ?", (ISBN,))
        result = cursor.fetchone()

        if result[0] > 0:
            raise ValueError(f"ISBN: {ISBN} already exists in the database.")

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
    @staticmethod
    @use_db        
    def search(cursor,query):
        search_book = f'%{query.lower()}%' # 添加通配符以支持模糊查詢
        cursor.execute('SELECT * FROM book WHERE LOWER(book_name) LIKE ? OR LOWER(author) LIKE ?',(search_book,search_book))
        results = cursor.fetchall()
        
        if results is None or len(results) == 0: # 使用 is None 判斷查詢結果是否為 None
            logging.warning(f"Book name/author {search_book} does not exist.")
            return None  # 不存在
           
        book_data = []
        
        for book in results:
            book_data.append({
                "book_id": book[0],
                "book_name": book[1],
                "ISBN": book[2],
                "author": book[3],
                "version": book[4],
                "public_year": book[5],
                "publisher": book[6],
                "create_time": book[7]})
            
        logging.info(f"Books with query '{query}' retrieved successfully.")
        
        return book_data    

        
        
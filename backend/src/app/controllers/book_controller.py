from flask import jsonify, request
import logging
from app.services.book_service import BookService

class BookController:
    def add_book(self):
        logging.info("----Book_controller.add_book----")

        data = request.get_json()

        isbn = data.get('ISBN')
        book_name = data.get('book_name')
        author = data.get('author') 
        public_year = data.get('public_year')
        publisher = data.get('publisher')
        book_picture_url = data.get('book_picture_url')
        genre_id = data.get('genre_id')

        book = BookService.adding_book(isbn, book_name, author, public_year, publisher, book_picture_url, genre_id)
        return jsonify({
            'book_id': book['book_id'],
            'ISBN': book['ISBN'],
            'book_name': book['book_name'],
            'author': book['author'],
            'public_year': book['public_year'],
            'publisher': book['publisher'],
            'book_picture_url' : book['book_picture_url'],
            "genre_id": book['genre_id']
        }), 201
        
    def update_book(self):
        logging.info("----Book_controller.update_book----")

        # TODO: 實現修改書籍邏輯
        return jsonify({"message": "Book updated successfully"})
    
    def get_books(self):
        logging.info("----Book_controller.get_books----")

        # TODO: 實現獲得書籍資料邏輯
        return jsonify({"message": "Books retrieved successfully", "books": []})
    
    def get_booklist(self):
        logging.info("----Book_controller.list_books----")

        # TODO: 實現獲得書籍列表邏輯
        genre_id = request.args.get('genre_id')
        book_list = BookService.get_all_books() if genre_id is None else BookService.get_all_books_by_genre(genre_id)
        return book_list, 200

    def search_books(self):
        logging.info("----Book_controller.search_books----")

        # TODO: 實現書籍搜尋邏輯
        return jsonify({"message": "Books searched successfully", "books": []})
    
    def get_book_by_isbn():
        isbn = request.args.get('isbn') 
        if not isbn:
            return jsonify({"message": "ISBN is required"}), 400

        # 查詢資料庫
        book = db.session.execute(
            "SELECT * FROM Books WHERE ISBN = :isbn",
            {"isbn": isbn}
        ).fetchone()

        if not book:
            return jsonify({"message": "Book not found"}), 404

        # 返回書籍資料
        return jsonify({
            "isbn": book.ISBN,
            "book_name": book.BookName,
            "author": book.Author,
            "public_year": book.PublicYear,
            "publisher": book.Publisher,
            "book_picture_url": book.BookPictureUrl
        }), 200
    
book_controller = BookController()
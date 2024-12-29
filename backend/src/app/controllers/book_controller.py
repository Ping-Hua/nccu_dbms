from flask import jsonify,request
import logging
from app.services.book_service import BookService

class BookController:
    def add_book(self):
        logging.info("----Book_controller.add_book----")

        # TODO: 實現新增書籍邏輯
        return jsonify({"message": "Book added successfully"})
    
    def update_book(self):
        logging.info("----Book_controller.update_book----")

        # TODO: 實現修改書籍邏輯
        return jsonify({"message": "Book updated successfully"})
    
    def get_books(self):
        logging.info("----Book_controller.get_books----")

        # TODO: 實現獲得書籍資料邏輯
        return jsonify({"message": "Books retrieved successfully", "books": []})
    
    def list_books(self):
        logging.info("----Book_controller.list_books----")

        # TODO: 實現獲得書籍列表邏輯
        return jsonify({"message": "Books listed successfully", "books": []})
    
    def search_books(self):
        logging.info("----Book_controller.search_books----")
        book_name = request.args.get("book_name")  # 假設從查詢參數中獲取書名
        if not book_name:
            logging.warning("Book name is missing in the request.")
            return jsonify({"success": False, "error": "Book name is required"}), 400

        try:
             # 使用實例化的 Service 來調用 search 方法
            book_service = BookService()
            searching = book_service.search(book_name)
            if searching:
                logging.info(f"Books with query '{book_name}' retrieved successfully.")
                return jsonify({"success": True, "message": "Books searched successfully", "book": searching}), 200
                 
            else:
                logging.warning(f"Attempted to search non-existent book with  {book_name}")
                return jsonify({"success": False, "error": "Books not found"}),404
        except Exception as e:
            logging.error(f"Error occurred while searching book with {book_name}: {str(e)}")
            return jsonify({"success": False, "error": str(e)}),500
        
        # TODO: 實現書籍搜尋邏輯
        # return jsonify({"message": "Books searched successfully", "books": []})
    
book_controller = BookController()
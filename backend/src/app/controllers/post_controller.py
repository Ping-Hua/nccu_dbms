from flask import jsonify, request
import logging
from app.services.post_service import PostService

class PostController:
    def add_post(self):
        logging.info("----post_controller.add_post----")
        
        data = request.get_json()
        seller_user_id = data.get('seller_user_id')
        book_id = data.get('book_id')
        book_condition = data.get('book_condition')
        price = data.get('price')

        if not all([seller_user_id, book_id, book_condition]):
            return jsonify({"error": "Missing required fields: seller_user_id, book_id, book_condition"}), 400
        if not isinstance(price, (int, float)) or price <= 0:
            return jsonify({"error": "Price must be a positive integer"}), 400
        
        try:
            post = PostService.add_post(seller_user_id, book_id, book_condition, price)
            return jsonify({
                'post_id': post['post_id'],
                'seller_user_id': post['seller_user_id'],
                'book_id': post['book_id'],
                'book_condition': post['book_condition'],
                'price': post['price'],
                'create_time': post['create_time']
            }), 201
        
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(f"Error adding post: {str(e)}")
            return jsonify({"error": "An unexpected error occurred."}), 500
    
    def update_post(self):
        logging.info("----Post_controller.update_post----")

        # TODO: 實現修改貼文邏輯
        return jsonify({"message": "Post updated successfully"})
    
    def delete_post(self):
        logging.info("----Post_controller.delete_post----")

        # TODO: 實現刪除貼文邏輯
        return jsonify({"message": "Post deleted successfully"})
    
post_controller = PostController()

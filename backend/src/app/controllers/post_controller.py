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
        data = request.get_json()
        post_id = data.get('post_id')
        book_id = data.get('book_id')
        book_condition = data.get('book_condition')
        price = data.get('price')

        if not post_id:
            return jsonify({"error": "Missing required fields: post_id"}), 400
        
        try:
            post = PostService.get_post(post_id)

            book_id = PostService.update_post_book(post_id, book_id)['book_id'] if book_id else post["book_id"]
            book_condition = PostService.update_post_book_condition(post_id, book_condition)['book_condition'] if book_condition else post["book_condition"]
            price = PostService.update_post_price(post_id, price)['price'] if price else post["price"]

            post = {
                "post_id" : post_id,
                "book_id" : book_id,
                "book_condition" : book_condition,
                "price" : price
            }

            return post, 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logging.error(f"Error adding post: {str(e)}")
            return jsonify({"error": "An unexpected error occurred." + str(e)}), 500
    
    def delete_post(self,post_id):
        logging.info("----Post_controller.delete_post----")
        try:
            # 呼叫 service 層進行刪除，並獲取被刪除的貼文資料
            deleted_post = PostService.service_delete_post(post_id)
            if deleted_post:
                logging.info(f"Post with ID {post_id} deleted successfully: {deleted_post}")
                return {"success": True, "message": "Post deleted successfully", "post": deleted_post}, 200
            else:
                logging.warning(f"Attempted to delete non-existent post with ID {post_id}")
                return {"success": False, "error": "Post not found"},404
        except Exception as e:
            logging.error(f"Error occurred while deleting post with ID {post_id}: {str(e)}")
            return {"success": False, "error": str(e)},500

    def get_post(self, post_id):
        logging.info("----Post_controller.get_post----")
        post = PostService.get_post(post_id)
        return post, 201
    
    def get_all_post(self):
        logging.info("----Post_controller.get_all_post----")
        post_list = PostService.get_all_post()
        return post_list, 201

    

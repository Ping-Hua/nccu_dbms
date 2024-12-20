from flask import jsonify, request, g
import logging
from sqlite3 import IntegrityError
from app.database import get_db

class PostController:
    def add_post(self):
        logging.info("----- PostController.add_post -----")
        try:
            user_id = g.user_id  
            if not user_id:
                return jsonify({"error": "User not authenticated"}), 401

            data = request.get_json()
            price = data.get('BookPrice') 
            book_condition = data.get('BookCondition')  

            if not price or not book_condition:
                return jsonify({
                    "error": "BookPrice and BookCondition are required fields"
                }), 400

            db = get_db()
            cursor = db.cursor()

            cursor.execute(
                (user_id, price, book_condition)
            )
            db.commit()

            post_id = cursor.lastrowid
            return jsonify({
                "message": "Post added successfully",
                "PostID": post_id
            }), 201

        except IntegrityError as e:
            logging.error(f"Database error: {e}")
            return jsonify({"error": "Database integrity error"}), 400

        except Exception as e:
            logging.error(f"Error adding post: {e}")
            return jsonify({"error": "Internal Server Error"}), 500
    
    def update_post(self):
        logging.info("----Post_controller.update_post----")

        # TODO: 實現修改貼文邏輯
        return jsonify({"message": "Post updated successfully"})
    
    def delete_post(self):
        logging.info("----Post_controller.delete_post----")

        # TODO: 實現刪除貼文邏輯
        return jsonify({"message": "Post deleted successfully"})
    
post_controller = PostController()

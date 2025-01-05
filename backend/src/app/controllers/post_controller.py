from flask import jsonify, request
import logging
from app.services.post_service import PostService
from app.errors.custom_exceptions import ResourceNotFoundError, ValidationError

class PostController:
    def add_post(self):
        logging.info("----post_controller.add_post----")
        
        data = request.get_json()
        seller_user_id = data.get('seller_user_id')
        book_id = data.get('book_id')
        book_condition = data.get('book_condition')
        price = data.get('price')
        
        post = PostService.add_post(seller_user_id, book_id, book_condition, price)
        return jsonify({
            'post_id': post['post_id'],
            'seller_user_id': post['seller_user_id'],
            'book_id': post['book_id'],
            'book_condition': post['book_condition'],
            'price': post['price'],
        }), 201

    def update_post(self):
        logging.info("----Post_controller.update_post----")
        data = request.get_json()
        post_id = data.get('post_id')
        book_id = data.get('book_id')
        book_condition = data.get('book_condition')
        price = data.get('price')
        
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
    
    def delete_post(self,post_id):
        logging.info("----Post_controller.delete_post----")

        # 呼叫 service 層進行刪除，並獲取被刪除的貼文資料
        deleted_post = PostService.service_delete_post(post_id)

        # if deleted_post is None:
        #     raise ResourceNotFoundError(f"Attempted to delete non-existent post with ID {post_id}")
        logging.info(f"Post with ID {post_id} deleted successfully: {deleted_post}")
        return {"success": True, "message": "Post deleted successfully", "post": deleted_post}, 200

        

    def get_post(self, post_id):
        logging.info("----Post_controller.get_post----")
        post = PostService.get_post(post_id)
        if post is None:
            raise ResourceNotFoundError("Unable to find the target post with the specified post_id")
        return post, 200
    
    def get_all_post(self):
        logging.info("----Post_controller.get_all_post----")
        book_id = request.args.get('book_id')
        if book_id:
            post_list = PostService.get_all_post_by_book(book_id)
        else:
            post_list = PostService.get_all_post()

        if post_list is None:
            raise ResourceNotFoundError("Unable to find the post_list")
        
        return post_list, 200
    

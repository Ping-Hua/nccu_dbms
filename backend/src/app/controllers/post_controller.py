from flask import jsonify, request, session
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

        book_id = post["book_id"] if book_id is None else PostService.update_post_book(post_id, book_id)['book_id']
        book_condition = post["book_condition"] if book_condition is None else PostService.update_post_book_condition(post_id, book_condition)['book_condition']
        price = post["price"] if price is None else PostService.update_post_price(post_id, price)['price']

        post = {
            "post_id" : post_id,
            "book_id" : book_id,
            "book_condition" : book_condition,
            "price" : price
        }

        return post, 201
    def user_post(self):
        logging.info("----PostController.user_post----")
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({"message": "Missing required field: user_id"}), 400

        try:
            user_post = PostService.get_posts_by_user(user_id)
            if not user_post:
                return jsonify({"message": f"No post found for the userID: {user_id}.", "user_post": []}), 200

            return jsonify({ "user_post" : user_post }), 200

        except Exception as e:
            logging.error(f"Error getting user's post: {str(e)}")
            return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


    def get_post(self, post_id):
        logging.info("----Post_controller.get_post----")
        post = PostService.get_post(post_id)
        return post, 200

    def get_all_post(self):
        logging.info("----Post_controller.get_all_post----")
        book_id = request.args.get('book_id')
        post_list = PostService.get_all_post() if book_id is None else PostService.get_all_post_by_book(book_id)
        return post_list, 200

post_controller = PostController()
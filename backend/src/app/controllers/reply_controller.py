from flask import jsonify, request
import logging
from app.services.reply_service import ReplyService


class ReplyController:
    def add_reply(self):
        logging.info("----Reply_controller.add_reply----")

        data = request.get_json()
        from_user_id = data.get('from_user_id') # 回應者的 user 的 userId
        to_user_id = data.get('to_user_id') # 貼文 user 的 userId
        post_id = data.get('post_id') # 貼文的 ID
        message = data.get('message') # 回應的文字

        if not all([from_user_id, to_user_id, post_id, message]):
            return jsonify({"error": "Missing required fields: from_user_id, to_user_id, post_id, message"}), 400
        
        try:
            reply = ReplyService.add_reply(from_user_id, to_user_id, post_id, message)
            return jsonify({
                'reply_id': reply['reply_id'],
                'from_user_id': reply['from_user_id'],
                'to_user_id': reply['to_user_id'],
                'post_id': reply['post_id'],
                'message': reply['message'],
                'reply_time': reply['reply_time'],
            }), 201
        
        except Exception as e:
            logging.error(f"Error adding reply: {str(e)}")
            return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
    
    def history(self):
        logging.info("----Reply_controller.history----")
        seller_user_id = request.args.get('seller_user_id') 
        buyer_user_id = request.args.get('buyer_user_id') 
        post_id = request.args.get('post_id') # 貼文的 ID
        
        if not all([seller_user_id, buyer_user_id, post_id]):
            return jsonify({"error": "Missing required fields: seller_user_id, buyer_user_id, post_id"}), 400
        
        try:
            reply_history = ReplyService.get_reply_history(seller_user_id, buyer_user_id, post_id)
            return jsonify({ "reply_history" : reply_history }), 201
        
        except Exception as e:
            logging.error(f"Error getting reply history: {str(e)}")
            return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
        
    def user_history(self):
        logging.info("----Reply_controller.user_history----")
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({"error": "Missing required fields: user_id"}), 400
        
        try:
            reply_history = ReplyService.get_user_all_history(user_id)

            if not reply_history:
                return jsonify({"message": f"No reply history found for the userID: {user_id}.", "reply_history": []}), 200
            
            return jsonify({ "reply_history" : reply_history["reply_history"], "total_reply_count": reply_history["total_reply_count"]}), 200
        
        except Exception as e:
            logging.error(f"Error getting user's reply history: {str(e)}")
            return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


reply_controller = ReplyController()
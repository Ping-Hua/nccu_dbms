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
                'reply_time': reply['reply_time']            
            }), 201
        
        except Exception as e:
            logging.error(f"Error adding reply: {str(e)}")
            return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
    
    def private_message(self):
        logging.info("----Reply_controller.private_message----")

        # TODO: 實現一對一留言邏輯
        return jsonify({"message": "Private message sent successfully"})
    
    def reply_notification(self):
        logging.info("----Reply_controller.reply_notification----")

        # TODO: 實現回應通知邏輯
        return jsonify({"message": "Reply notification sent successfully"})
    
    def history(self):
        logging.info("----Reply_controller.history----")

        # TODO: 實現留言歷史紀錄
        return jsonify({"message": "Reply history retrieved successfully", "replies": []})

reply_controller = ReplyController()
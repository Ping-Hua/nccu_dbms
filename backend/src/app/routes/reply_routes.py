from flask import Blueprint
from app.controllers.reply_controller import reply_controller

reply_bp = Blueprint('reply', __name__)

reply_bp.add_url_rule('/add_reply', view_func=reply_controller.add_reply, methods=['POST'])
reply_bp.add_url_rule('/history', view_func=reply_controller.history, methods=['GET'])
reply_bp.add_url_rule('/user_history', view_func=reply_controller.user_history, methods=['GET']) 
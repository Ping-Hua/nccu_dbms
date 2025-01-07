from flask import Blueprint
from app.controllers.post_controller import PostController

post_bp = Blueprint('post', __name__)

# 建立控制器實例
post_controller = PostController()

post_bp.add_url_rule('/add_post', view_func=post_controller.add_post, methods=['POST'])
post_bp.add_url_rule('/get_post/<int:post_id>', view_func=post_controller.get_post, methods=['GET'])
post_bp.add_url_rule('/get_post', view_func=post_controller.get_all_post, methods=['GET'])
post_bp.add_url_rule('/update_post', view_func=post_controller.update_post, methods=['PUT'])
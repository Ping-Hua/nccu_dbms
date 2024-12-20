from flask import jsonify
import logging
from app.services.post_service import PostService
## api 中的
class PostController:
    def add_post(self):
        logging.info("----Post_controller.add_post----")

        # TODO: 實現新增貼文邏輯
        return jsonify({"message": "Post added successfully"})
    
    def update_post(self):
        logging.info("----Post_controller.update_post----")

        # TODO: 實現修改貼文邏輯
        return jsonify({"message": "Post updated successfully"})
    
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
        # TODO: 實現刪除貼文邏輯
        # return jsonify({"message": "Post deleted successfully"})
    

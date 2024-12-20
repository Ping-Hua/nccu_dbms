from app.database import get_db

class PostService:
    def service_delete_post(post_id):
        db = get_db()
        cursor = db.cursor()

        # 查找貼文
        cursor.execute('SELECT * FROM book_posts WHERE id = ?', (post_id,))
        post = cursor.fetchone()
        if post is None:
            return None  # 貼文不存在

        # 刪除貼文
        cursor.execute('DELETE FROM book_posts WHERE id = ?', (post_id,))
        db.commit()

         # 回傳刪除的貼文資訊
        return {"id": post["id"], "title": post["title"]}

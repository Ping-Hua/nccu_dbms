from database import db_session
from models import BookPost

def delete_post_service(post_id):
    # 查找貼文
    post = db_session.query(BookPost).filter_by(id=post_id).first()
    if not post:
        return False  # 貼文不存在

    # 刪除貼文
    db_session.delete(post)
    db_session.commit()
    return True

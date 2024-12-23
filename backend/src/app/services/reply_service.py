from app.database import get_db
import logging

class ReplyService:
    def add_reply(from_user_id, to_user_id, post_id, message):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO reply (from_user_id, to_user_id, post_id, message) VALUES (?, ?, ?, ?)", 
                (from_user_id, to_user_id, post_id, message)
            )
            db.commit()

            reply_id = cursor.lastrowid
            logging.info(f"Reply added successfully: {reply_id}")

            cursor.execute(
                "SELECT reply_id, from_user_id, to_user_id, post_id, message, create_time "
                "FROM reply WHERE reply_id = ?", 
                (reply_id,)
            )
            reply = cursor.fetchone()

            reply_data = {
                "reply_id": reply[0],
                "from_user_id": reply[1],
                "to_user_id": reply[2],
                "post_id": reply[3],
                "message": reply[4],
                "reply_time": reply[5]
            }
            return reply_data
        except Exception as e:
            db.rollback()
            raise e
        
    def get_reply_history(seller_user_id, buyer_user_id, post_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "SELECT reply_id, from_user_id, to_user_id, post_id, message, create_time "
                "FROM reply WHERE post_id = ? AND ((from_user_id = ? AND to_user_id = ?) OR (from_user_id = ? AND to_user_id = ?))"
                "ORDER BY create_time ASC", 
                (post_id, seller_user_id, buyer_user_id, buyer_user_id, seller_user_id)
            )
            replies = cursor.fetchall()
            reply_datas = []
            for reply in replies:
                reply_data = {
                    "reply_id": reply[0],
                    "from_user_id": reply[1],
                    "to_user_id": reply[2],
                    "post_id": reply[3],
                    "message": reply[4],
                    "reply_time": reply[5]
                }
                reply_datas.append(reply_data)
            return reply_datas
        except Exception as e:
            db.rollback()
            raise e
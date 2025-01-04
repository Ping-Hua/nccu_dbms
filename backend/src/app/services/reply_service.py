from app.database import use_db
import logging

class ReplyService:
    @use_db
    def add_reply(cursor, from_user_id, to_user_id, post_id, message):
        cursor.execute(
            "INSERT INTO reply (from_user_id, to_user_id, post_id, message) VALUES (?, ?, ?, ?)", 
            (from_user_id, to_user_id, post_id, message)
        )

        reply_id = cursor.lastrowid
        logging.info(f"Reply added successfully: {reply_id}")

        reply_data = {
            "reply_id": reply_id,
            "from_user_id": from_user_id,
            "to_user_id": to_user_id,
            "post_id": post_id,
            "message": message,
        }
        return reply_data
        
    @use_db
    def get_reply_history(cursor, seller_user_id, buyer_user_id, post_id):
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
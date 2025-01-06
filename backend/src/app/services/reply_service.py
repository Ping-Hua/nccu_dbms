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
    
    @use_db
    def get_user_all_history(cursor,user_id):
        cursor.execute(
            """ 
            -- （user_id, post_id） 分組、編號
            WITH LatestReplies AS (
                SELECT 
                    CASE
                        WHEN from_user_id = ? THEN to_user_id
                        ELSE from_user_id
                    END AS other_user_id,
                    post_id,
                    message,
                    create_time,
                    ROW_NUMBER() OVER (  -- 給唯一編號
                        PARTITION BY 
                            CASE 
                                WHEN from_user_id =? THEN to_user_id 
                                ELSE from_user_id 
                                END,
                                post_id
                            ORDER BY create_time DESC -- 降序（編號 1 會最新）
                    ) AS row_num
                FROM reply 
                WHERE from_user_id = ? OR to_user_id = ? -- 選跟 user_id 有關的 reply
            )
            SELECT other_user_id, post_id, message, create_time
            FROM LatestReplies
            WHERE row_num = 1
            ORDER by create_time DESC -- 降序，新到舊
            """,
            (user_id, user_id, user_id, user_id)
        )

        replies = cursor.fetchall()
        reply_datas = []

        for reply in replies:
            reply_data = {
                "other_user_id": reply[0],
                "post_id": reply[1],
                "message": reply[2],
                "reply_time": reply[3]
            }
            reply_datas.append(reply_data)

        return reply_datas
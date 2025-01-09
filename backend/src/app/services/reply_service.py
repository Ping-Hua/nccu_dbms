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

        # 新增回應時間
        cursor.execute("SELECT create_time FROM reply WHERE reply_id = ?", (reply_id,))
        create_time_row = cursor.fetchone()
        reply_time = create_time_row['create_time'] if create_time_row else None

        reply_data = {
            "reply_id": reply_id,
            "from_user_id": from_user_id,
            "to_user_id": to_user_id,
            "post_id": post_id,
            "message": message,
            "reply_time": reply_time,
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
            SELECT lr.other_user_id, lr.post_id, lr.message, lr.create_time, b.book_name
            FROM LatestReplies lr
            LEFT JOIN post p ON lr.post_id = p.post_id -- jlin reply & post 表
            LEFT JOIN book b ON p.book_id = b.book_id -- join book & post 表
            WHERE lr.row_num = 1
            ORDER by lr.create_time DESC -- 降序，新到舊
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
                "reply_time": reply[3],
                "book_name": reply[4]  
            }
            reply_datas.append(reply_data)

        return {"reply_history" : reply_datas, "total_reply_count": len(reply_datas)}
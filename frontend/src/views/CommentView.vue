<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';

const apiUrl = import.meta.env.VITE_BE_API_BASE_URL; 
const userID = 666; 

const comments = reactive([]); // 留言板列表
const selectedPostId = ref(null); // 留言板 postID
const commentHistory = reactive([]); // 留言板內容

// ---- 留言列表 ----
const fetchUserComments = async () => {
    console.log('Fetching comments for user:', userID);
    try {
      const { data } = await axios.get(`${apiUrl}/reply/user_history`, {
        params: { user_id: userID },
      });

      if (data && Array.isArray(data.reply_history)) {
        comments.length = 0; 
        data.reply_history.forEach((item) => comments.push(item)); 
        console.log('Loaded comments:', comments);
      } else {
        console.log('No comments found for the user.');
      }
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
    };

// ---- 單個留言板 ----
const fetchCommentHistory = async (postId, sellerUserId, buyerUserId) => {
  console.log('Fetching comment history for post:', postId);
  try {
    const { data } = await axios.get(`${apiUrl}/reply/history`, {
      params: {
        post_id: postId,
        seller_user_id: sellerUserId,
        buyer_user_id: buyerUserId,
      },
    });

    if (data && Array.isArray(data.reply_history)) {
      commentHistory.length = 0; 
      data.reply_history.forEach((item) => commentHistory.push(item)); 
      console.log('Loaded comment history:', commentHistory);
    } else {
      console.log('No comments found for the post.');
    }
  } catch (error) {
    console.error('Error fetching comment history:', error);
  }
};

// ---- 點擊留言板 ----
const selectComment = (postId, sellerUserId, buyerUserId) => {
  selectedPostId.value = postId; // 留言板 ID
  fetchCommentHistory(postId, sellerUserId, buyerUserId); // 留言板內容
};

onMounted(async () => {
  await fetchUserComments(); 
  await selectComment();
});
</script>

<template>
    <div class="chat-container">
        <! -- 留言板列表 -- >
        <div class="chat-list">
            <h3>留言板列表</h3>
            <ul>
                <li v-for="comment in comments" :key="comment.post_id">
                    <p>{{ comment.to_user_id }}</p>
                    <p>message： {{ comment.message }}</p>
                </li>
            </ul>
        </div>
        <! -- 留言板內容 -- >
        <div class="chat-details">
            <ul>
                <li v-for="reply in replyHistory" :key="comment.reply_id">
                    <p>{{ reply.reply_user_id }}</p>
                    <p>message： {{ reply.reply_message }}</p>
                </li>
            </ul>
        </div>
    </div>
</template>

<style>
.chat-container {
    width: 100%;
    height: 80vh;
}

.chat-list {
    float: left;
    width: 300px;
    height: 100%; 
    background-color: #f0f0f0; 
    border-right: 1px solid #ddd; 
    padding: 0; 
    overflow-y: auto;
    margin: 0;
}

.chat-list h3 {
    font-size: 30px;
    margin: 20px 0; /* 垂直方向的間距 */
    text-align: center;
    color: #333; /* 標題文字顏色 */
}

.chat-list ul {
  list-style: none; 
  padding: 0;
  margin: 0;
}

.chat-list li {
  padding: 10px 15px;
  background-color: #ffffff; 
  border-radius: 8px; 
  margin: 10px; 
  border: 1px solid #ddd; 
  transition: background-color 0.3s;
  cursor: pointer;
}

.chat-list li:hover {
  background-color: #e6f7ff; 
}

.chat-list li p {
  margin: 0;
  color: #555; 
  font-size: 14px;
}

.chat-details {
    margin-left: 1000px;
    height: 100%;
    background-color: #ffffff;
    padding: 20px;
    box-sizing: border-box;
}
</style>
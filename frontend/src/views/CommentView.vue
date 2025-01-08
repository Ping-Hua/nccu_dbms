<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';

const apiUrl = import.meta.env.VITE_BE_API_BASE_URL; 
const userID = 666;

const comments = reactive([]); // 留言板列表
const selectedPostId = ref(null); // 留言板 postID
const selectedUserId = ref(null); // 留言板 對象 UserID
const commentHistory = reactive([]); // 留言板內容
const commentsCount = ref(-1); // 留言表列表留言數量
const newMessage = ref('');

// ---- 留言列表 ----
const fetchCommentsList = async () => {
    console.log('Fetching comments List for user:', userID);
    try {
      const { data } = await axios.get(`${apiUrl}/reply/user_history`, {
        params: { user_id: userID },
      });

      if (data && Array.isArray(data.reply_history)) {
        comments.length = 0; 
        data.reply_history.forEach((item) => comments.push(item)); 
        commentsCount.value = data.total_reply_count;  // 留言數量
        console.log('getting comments List successful');
      } else {
        commentsCount.value = 0
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
const selectComment = (postId, otherUserId) => {
    console.log('Selecting comment with postId:', postId, 'otherUserId:', otherUserId);
    selectedUserId.value = otherUserId;
    selectedPostId.value = postId; // 留言板 ID
    fetchCommentHistory(postId, userID, otherUserId); // 留言板內容
};

// ---- 傳送留言 ----
const addReply = async () => {
    console.log('Sending reply with postId:', selectedPostId.value);

    try {
        const payload = {
            from_user_id: userID,
            to_user_id: selectedUserId.value,
            post_id: selectedPostId.value,
            message: newMessage.value,
        };

        const { data } = await axios.post(`${apiUrl}/reply/add_reply`, payload);
        console.log('Reply added successfully');

        newMessage.value = '';

        commentHistory.push(data);
    } catch (error) {
        console.error('Error sending reply:', error);
    }
};


onMounted(async () => {
    await fetchCommentsList(); 
});
</script>

<template>
    <div class="comment-container-fluid d-flex flex-row m-0 p-0 h-100 w-100" style="height: 100%;">
        <! ---- 留言板列表 ---->
        <div 
            class="comment-board pe-3 border-end" 
            style="width:30% ; overflow-y: auto; background-color: #f8f9fa; height: 100%; border: 2px solid #343a40;" 
        >
            <div class="comment-board-header">
                <h5 class="m-0 pt-3 pb-2 ps-2">留言板列表</h5>
            </div>
            <div 
                v-if="commentsCount > 0" 
                v-for="comment in comments" 
                :key="`comment-${comment.id}`" 
                class="comment-card my-2 p-2 rounded shadow-sm"
                @click="selectComment(comment.post_id, comment.other_user_id)"
            >
                <!-- UserID -->
                <strong class="d-block">
                    User: {{ comment.other_user_id }}
                </strong>

                <!-- PostID -->
                <strong class="badge rounded-pill bg-secondary mb-1">
                    Book Name: {{ comment.book_name }}
                </strong>

                <!-- message -->
                <p class="m-0 text-truncate">{{ comment.message }}</p>
            </div>
            <!-- 沒有留言 -->
            <div 
                v-else 
                class="d-flex justify-content-center align-items-center" 
                style="height: calc(100% - 50px);"
            >
                <p class="text-muted text-center">還沒有人留言，您也還未使用留言功能 (｡ ︿ ｡)</p>
            </div>
        </div>

        <! ---- 留言板內容 ---->
        <div class="comment ps-3 d-flex flex-column" style="width:70%; height: 100%; overflow-y: auto;">
            <h5 class="m-0 pt-3 pb-2 ps-2">留言板</h5>

            <!-- 未點擊聊天室 -->
            <div 
                v-if="!selectedPostId" 
                class="d-flex justify-content-center align-items-center flex-fill"
                style="height: calc(100% - 70px);"
            >
                <p class="text-muted text-center">點擊左側列表，進入留言板！</p>
            </div>

            <!-- 顯示留言內容 -->
            <div v-else class="message-container px-3 py-2 overflow-auto" ref="messagesContainer">
                <transition-group name="fade" tag="div">
                    <div 
                        class="message d-flex flex-column"
                        v-for="(message,index) in commentHistory" 
                        :key="index"
                    >
                        <!-- 自己的訊息 -->
                        <div v-if="message.from_user_id === userID" class="d-flex justify-content-end mb-3">
                            <div class="message-body bg-secondary text-white p-2 rounded text-end float-end">
                                {{ message.message }}
                            </div>
                        </div>

                        <!-- 對方的訊息 -->
                        <div v-else class="d-flex justify-content-start mb-3">
                            <div class="d-flex flex-column align-items-start">
                                <strong style="font-size: 0.85rem; margin-bottom: 5px;">{{ message.from_user_id }}</strong>
                                <div class="message-body bg-secondary text-white p-2 rounded">
                                {{ message.message }}
                                </div>
                            </div>
                        </div>
                    </div>
                </transition-group>
            </div>

            <!-- 留言輸入欄 -->
            <div v-if="selectedPostId" class="input-group mt-2" style="position: absolute; bottom: 20px; width: 68%;">
                <input v-model="newMessage" type="text" class="form-control" placeholder="輸入您的回覆..." style="border-radius: 15px; padding: 10px;">
                <button 
                    class="btn btn-secondary" @click="addReply" 
                    :disabled="!newMessage.trim()" 
                    style="margin-left: 10px; border-radius: 15px; padding: 8px 16px;"
                > Send </button>
            </div>
        </div>
    </div>
</template>

<style>
.flex-fill {
  flex: 1 1 auto; 
  height: 100%;   
}

<style>
.text-truncate {
  white-space: nowrap; /* 不換行 */
  overflow: hidden;    /* 隱藏溢出文字 */
  text-overflow: ellipsis; /* 超出部分顯示為 ... */
}
</style>
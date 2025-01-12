<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useGlobalStore } from '../stores/global.js';

const apiUrl = import.meta.env.VITE_BE_API_BASE_URL;
const globalStore = useGlobalStore();

const userID = globalStore.user.id;

const book = ref({});
const bookId = ref(null);
bookId.value = this.$route.params.bookId;
const posts = ref([]);

// ---- 取得書籍資訊 ----
const fetchBookDetails = async () => {
    try {
        console.log("Fetching book details for book_id:", bookId.value);
        const { data } = await axios.get(`${apiUrl}/book/details`, {
        params: { book_id: bookId.value },
        });

        
        book.value = {
            BookPictureUrl: data.book_picture_url,
            BookName: data.book_name,
            Author: data.author,
            PublicYear: data.public_year,
            Publisher: data.publisher,
        };

        console.log("Book details fetched successfully:", book.value);
    } catch (error) {
        console.error("Error fetching book details:", error);
        alert("Failed to fetch book details. Please try again.");
    }
};

// ---- 取得該書籍的 Post ----
const fetchPosts = async () => {
    try {
        console.log("Fetching posts for book_id:", bookId.value);
        const { data } = await axios.get(`${apiUrl}/post/get_post`, {
            params: { book_id: bookId.value },
        });

        // 整理 Post 資料
        posts.value = Array.isArray(data)
            ? data.map((post) => ({
                  post_id: post.post_id,
                  seller: `${post.seller_user_id}`,
                  postDate: new Date(post.create_time).toLocaleDateString(),
                  condition: post.book_condition,
                  price: post.price,
              }))
            : [];

        console.log("Posts fetched successfully:", posts.value);
    } catch (error) {
        console.error("Error fetching posts:", error);
        alert("Failed to fetch posts. Please try again.");
    }
};

// ---- add post 變數 ----
const showAddPostModal = ref(false);
const newPost = ref({
    seller_user_id: userID,
    book_id: bookId.value,
    condition: "",
    price: null,
});

// ---- 新增 Post ----
const addPost = async () => {
    try {
        const { data } = await axios.post(`${apiUrl}/post/add_post`, {
            seller_user_id: newPost.value.seller_user_id,
            book_id: bookId.value,
            book_condition: newPost.value.condition,
            price: newPost.value.price,
        });

        fetchPosts();
        alert("Post added successfully!");
        
        // 清空
        showAddPostModal.value = false;
        newPost.value = {
            seller_user_id: userID,
            book_id: bookId.value,
            condition: "",
            price: null,
        };
    } catch (error) {
        console.error("Error adding post:", error);
        alert("Failed to add post. Please try again.");
    }
};

// ---- Reply 變數 ----
const showReplyModal = ref(false);
const currentPost = ref(null);
const newReply = ref("");

// ---- 開啟 Reply Modal ----
const openReplyModal = (post) => {
    currentPost.value = post; 
    console.log("currentPost in openReplyModal:", currentPost.value); // 打印 currentPost
    showReplyModal.value = true; 
};

// ---- 新增 Reply ----
const sendReply = async () => {
    if (!newReply.value.trim()) {
        alert("Message cannot be empty!");
        return;
    }

    try {
        await axios.post(`${apiUrl}/reply/add_reply`, {
            from_user_id: userID,
            to_user_id: currentPost.value.seller,
            post_id: currentPost.value.post_id,
            message: newReply.value.trim(),
        });

        alert("Reply sent successfully!");

        newReply.value = "";
        showReplyModal.value = false;
    } catch (error) {
        console.error("Error sending reply:", error);
        alert("Failed to send reply. Please try again.");
    }
};

const closeReplyModal = () => {
    showReplyModal.value = false;
    currentPost.value = null;
    newReply.value = "";
};

onMounted(() => {
    fetchBookDetails();
    fetchPosts();
});
</script>





<template>
  <div class="home">
    <div class="post-page">
      <div class="book-info">
        <img :src="book.BookPictureUrl" alt="Book Cover" class="book-cover" />
        <div class="book-details">
          <h2 class="book-title">{{ book.BookName }}</h2>
          <p class="book-meta"><strong>Author:</strong> {{ book.Author }}</p>
          <p class="book-meta"><strong>Publication Year:</strong> {{ book.PublicYear }}</p>
          <p class="book-meta"><strong>Publisher:</strong> {{ book.Publisher }}</p>
        </div>
      </div>
      <hr />
      <div class="post-section">
        <div class="post-header">
          <h4><b>Seller Posts</b></h4>
          <button @click="showAddPostModal = true" class="btn btn-secondary">+ Add Post</button>
        </div>

        <table class="posts-table">
          <thead>
            <tr>
              <th>Seller</th>
              <th>Post Date</th>
              <th>Book Condition</th>
              <th>Price</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="post in posts" :key="post.id">
              <td>{{ post.seller }}</td>
              <td>{{ post.postDate }}</td>
              <td>{{ post.condition }}</td>
              <td>${{ post.price }}</td>
              <td>
                <button @click="openReplyModal(post)" class="btn btn-secondary">Reply</button>
              </td>
            </tr>
          </tbody>
        </table>
    </div>

  <div v-if="showAddPostModal" class="modal-overlay" @click.self="showAddPostModal = false">
    <div class="modal-content">
      <h4>Add Post</h4>
      <form @submit.prevent="addPost">
        <div class="form-group">
          <label for="condition">Book Condition:</label>
          <input
            type="text"
            id="condition"
            v-model="newPost.condition"
            required
            placeholder="Enter book condition"
          />
        </div>
        <div class="form-group">
          <label for="price">Price:</label>
          <input
            type="number"
            id="price"
            v-model="newPost.price"
            required
            placeholder="Enter price"
          />
        </div>
        <div class="button-group">
          <button type="submit" class="btn-submit">Submit</button>
          <button type="button" class="btn-cancel" @click="showAddPostModal = false">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <div v-if="showReplyModal" class="modal-overlay" @click.self="showReplyModal = false">
    <div class="modal-content">
        <!-- 上半部分：Post 資訊 -->
        <div class="post-details">
            <h4>Reply</h4>
            <p><b>Seller:</b> {{ currentPost?.seller }}</p>
            <p><b>Price:</b> ${{ currentPost?.price }}</p>
            <p><b>Condition:</b> {{ currentPost?.condition }}</p>
        </div>
        <hr />

        <!-- 下半部分：Reply 表單 -->
        <form @submit.prevent="sendReply">
            <textarea
                v-model="newReply"
                placeholder="Type your reply here..."
                rows="4"
                required
            ></textarea>
            <div class="button-group">
                <button type="submit" class="btn-submit">Send Reply</button>
                <button type="button" class="btn-cancel" @click="closeReplyModal">Cancel</button>
            </div>
        </form>
    </div>
</div>

</div>
  </div>
</template>


<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.post-page {
padding: 70px;
margin-top: -80px;
}

/* 整體容器樣式 */
.book-info {
display: flex;
align-items: flex-start; 
background-color: #ffffff;
border-radius: 10px;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
padding: 20px;
max-width: 700px;
margin: 20px auto;
font-family: 'Arial', sans-serif;
}

/* 書籍封面樣式 */
.book-cover {
width: 150px;
height: 200px;
border-radius: 8px;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
object-fit: cover; /* 確保圖片不會變形 */
}

/* 書籍詳細資訊樣式 */
.book-details {
margin-left: 20px;
text-align: left;
}

.book-title {
font-size: 24px;
font-weight: bold;
margin-bottom: 10px;
color: #333;
}

.book-meta {
font-size: 16px;
margin: 5px 0;
color: #555;
}

.book-meta strong {
color: #000;
}


hr {
margin: 20px 0;
}

.post-section {
margin-top: 20px;
}

.post-header {
display: flex;
justify-content: space-between;
align-items: center;
}

.posts-table {
width: 100%;
border-collapse: collapse;
margin-top: 15px;
margin-bottom: 200px;
}

.posts-table th,
.posts-table td {
border: 1px solid #ddd;
padding: 10px;
text-align: center;
}

.posts-table th {
background-color: #f4f4f4;
font-weight: bold;
}

.posts-table tr:nth-child(even) {
background-color: #f9f9f9;
}

.posts-table tr:hover {
background-color: #f1f1f1;
}

.modal-overlay {
position: fixed;
top: 0;
left: 0;
width: 100%;
height: 100%;
background-color: rgba(0, 0, 0, 0.5);
display: flex;
justify-content: center;
align-items: center;
}

.modal-content {
background-color: white;
padding: 20px;
border-radius: 8px;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
width: 400px;
}

.form-group {
margin-top: 10px;
margin-bottom: 10px;
display: flex;
}

.form-group label {
margin-right: 10px; 
font-weight: bold; 
}

.form-group input {
padding: 6px; 
font-size: 14px;
border: 1px solid #ccc; 
border-radius: 4px; 
}

.button-group{
margin-top: 20px;
}

.btn-submit {
background-color: #007bff;
color: white;
padding: 5px 10px;
border: none;
border-radius: 5px;
cursor: pointer;
}

.btn-submit:hover {
background-color: #3364a8;
}

.btn-cancel {
background-color: #aaa;
color: white;
padding: 5px 10px;
border: none;
border-radius: 5px;
cursor: pointer;
margin-left: 20px;
}

.btn-cancel:hover {
background-color: #888;
}

.conversation {
max-height: 400px;
overflow-y: auto;
margin-bottom: 15px;
}

.message {
margin: 5px 0;
padding: 10px;
border-radius: 8px;
max-width: 80%;
}

.message.sent {
background-color: #e0ffe0;
align-self: flex-end;
}

.message.received {
background-color: #f0f0f0;
align-self: flex-start;
}

.time {
font-size: 12px;
color: #888;
margin-top: 5px;
}

.no-history {
text-align: center;
color: #aaa;
margin: 10px 0;
font-style: italic;
}


</style>
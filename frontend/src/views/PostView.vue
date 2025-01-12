<template>
  <div class="home">
    <div class="post-page">
      <div class="book-info">
          <img :src="book.book_picture_url" alt="Book Cover" class="book-cover" />
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
          <button @click="showAddPostModal = true" class="add-post-button">+ Add Post</button>
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
              <td>{{ post.date }}</td>
              <td>{{ post.condition }}</td>
              <td>${{ post.price }}</td>
              <td>
                <button @click="replyToPost(post.id, post.seller_user_id)" class="reply-button">Reply</button>
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
      <h4>Conversation</h4>
      <div class="conversation">
        <p v-if="currentConversation.length === 0" class="no-history">
          No conversation history. Start a new chat!
        </p>
        <div
          v-for="message in currentConversation"
          :key="message.reply_id"
          class="message"
          :class="{ 'sent': message.from_user_id === currentUser.id, 'received': message.to_user_id === currentUser.id }"
        >
          <p>{{ message.message }}</p>
          <span class="time">{{ message.reply_time }}</span>
        </div>
      </div>
      <form @submit.prevent="sendReply(postId, sellerUserId)">
        <textarea v-model="newReply" placeholder="Type your message..." required></textarea>
        <div class="button-group">
          <button type="submit" class="btn-submit">Send</button>
          <button type="button" class="btn-cancel" @click="showReplyModal = false">Cancel</button>
        </div>
      </form>
    </div>
</div>

</div>
  </div>
</template>

<script> 
export default {
props: ['isbn'], // 接收書籍的 ISBN
data() {
return {
  book: {}, // 書籍資訊
  posts: [], // 貼文列表
  showAddPostModal: false, // 控制模態框顯示
  newPost: {
    condition: '',
    price: '',
  },
  currentUser: {
    id: '12345', // 假設當前用戶 ID
    name: 'Alice', // 假設當前用戶名稱
  },
  selectedBook: {
    id: '67890', // 假設書籍 ID
  },
  showReplyModal: false, 
  currentReplySellerId: null,
  currentReplySellerName: '',
  currentConversation: [],
  newMessageContent: '',
};
},

created() {
  const isbn = this.$route.params.isbn;
  console.log('ISBN received:', isbn);
  if (!isbn) {
    alert('No ISBN provided. Cannot display book details.');
    return;
  }
  this.fetchBookDetails(isbn); // 傳入 ISBN 獲取書籍資訊
  this.fetchPosts(); // 獲取該書的貼文
},
methods: {
  // 獲取書籍詳細資訊
  fetchBookDetails(isbn) {
  fetch(`/api/v1/book/details?isbn=${encodeURIComponent(isbn)}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Failed to fetch book details');
      }
      return response.json();
    })
    .then((data) => {
      this.book = {
        BookPictureUrl: data.book_picture_url,
        BookName: data.book_name,
        Author: data.author,
        PublicYear: data.public_year,
        Publisher: data.publisher,
      };
    })
    .catch((error) => {
      console.error('Error fetching book details:', error);
      alert('An error occurred while fetching the book details.');
    });
},


  // 獲取貼文
  fetchPosts() {
    fetch('/api/v1/post/get_all_post', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch posts');
        }
        return response.json();
      })
      .then((posts) => {
        // 假設後端返回的數據格式正確
        this.posts = posts.map((post) => ({
          id: post.id,
          status: post.status || 'Available',
          seller: this.getSellerName(post.seller_user_id), 
          date: post.create_time.split('T')[0],
          condition: post.condition,
          price: post.price,
        }));
        console.log('Posts fetched successfully:', this.posts);
      })
      .catch((error) => {
        console.error('Error fetching posts:', error);
        alert('Failed to fetch posts. Please try again.');
      });
  },


addPost() {

    if (!this.currentUser || !this.currentUser.id) {
      console.error('Error: Current user is not defined');
      alert('Please log in to create a post.');
      return;
    }

    if (!this.newPost || !this.newPost.condition || !this.newPost.price) {
    console.error('Error: New post data is incomplete');
    alert('Please fill out all required fields.');
    return;
    }

const newPostData = {
  seller_user_id: this.currentUser.id, 
  book_id: this.selectedBook.id,        
  book_condition: this.newPost.condition, 
  price: this.newPost.price,              
};

console.log('Sending New Post Data:', newPostData);

fetch('/api/v1/post/add_post', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(newPostData),
})
  .then((response) => {
    if (!response.ok) {
      throw new Error('Failed to create post');
    }
    return response.json();
  })
  
  .then((createdPost) => {
    this.posts.push({
      id: createdPost.post_id,
      status: 'Available', 
      seller: this.currentUser.name,       
      date: createdPost.create_time.split('T')[0],
      condition: createdPost.book_condition,
      price: createdPost.price,
    });

    this.newPost = { condition: '', price: '' };
    this.showAddPostModal = false;
    alert('Post added successfully!');
  })
  .catch((error) => {
    console.error(error);
    alert('Failed to add post. Please try again.');
  });
},

replyToPost(postId, sellerUserId) {
if (!this.currentUser || !this.currentUser.id) {
  alert('Please log in to reply.');
  return;
}

fetch(`/api/v1/reply/history?post_id=${encodeURIComponent(postId)}&seller_user_id=${encodeURIComponent(sellerUserId)}&buyer_user_id=${encodeURIComponent(this.currentUser.id)}`)
  .then((response) => {
    if (!response.ok) {
      throw new Error('Failed to fetch conversation history');
    }
    return response.json();
  })
  .then((data) => {
    this.currentConversation = data.reply_history || [];
    this.showReplyModal = true;
  })
  .catch((error) => {
    console.error('Error fetching conversation history:', error);
    this.currentConversation = [];
    this.showReplyModal = true;
  });

},

sendReply(postId, sellerUserId) {
if (!this.newReply) {
  alert('Message cannot be empty.');
  return;
}

const replyData = {
  from_user_id: this.currentUser.id,
  to_user_id: sellerUserId,
  post_id: postId,
  message: this.newReply,
};

fetch('/api/v1/reply/add_reply', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(replyData),
})
  .then((response) => {
    if (!response.ok) {
      throw new Error('Failed to send reply');
    }
    return response.json();
  })
  .then((createdReply) => {
    this.currentConversation.push({
      ...createdReply,
      reply_time: new Date().toISOString(),
    });
    this.newReply = ''; 
  })
  .catch((error) => {
    console.error('Error sending reply:', error);
    alert('Failed to send reply. Please try again.');
  });
},


}
};
</script>


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

.add-post-button {
border-radius: 5px;
cursor: pointer;
}

.add-post-button:hover {
border-color: #555555cf; 
background-color: #f0f0f0; 
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

.reply-button {
padding: 5px 10px;
background-color: #28a745;
color: white;
border: none;
border-radius: 5px;
cursor: pointer;
}

.reply-button:hover {
background-color: #0c5108;
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
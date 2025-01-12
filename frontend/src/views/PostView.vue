<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isbn = ref(route.params.isbn);
const book = ref({});
const posts = ref([]);
const showAddPostModal = ref(false);
const newPost = ref({
    condition: '',
    price: '',
});
const currentUser = ref({
    id: '12345',
    name: 'Alice',
});
const showReplyModal = ref(false);
const currentReplySellerId = ref(null);
const currentReplySellerName = ref('');
const currentConversation = ref([]);
const newMessageContent = ref('');

const fetchBookDetails = async (isbn) => {
    try {
        const response = await fetch(`/api/v1/book/details?isbn=${isbn}`);
        if (!response.ok) {
        throw new Error('Failed to fetch book details');
        }

        const data = await response.json();
        console.log('Fetched book details:', data);

        if (!data.ISBN) {
        throw new Error('No book data found');
        }

        book.value = {
        BookPictureUrl: data.book_picture_url,
        BookName: data.book_name,
        Author: data.author,
        PublicYear: data.public_year,
        Publisher: data.publisher || 'Unknown',
        };
    } catch (error) {
        console.error('Error fetching book details:', error);
        alert('Failed to fetch book details. Please try again.');
    }
};

const fetchPosts = async (isbn) => {
    try {
        console.log('Fetching posts for ISBN:', isbn);
        const response = await fetch(`/api/v1/post/get_isbn_post?isbn=${isbn}`);
        if (!response.ok) {
        throw new Error('Failed to fetch posts');
        }

        const data = await response.json();
        console.log('Fetched posts:', data);

        posts.value = data.map((post) => ({
        id: post.post_id,
        seller: `User ${post.seller_user_id}`,
        date: new Date(post.create_time.replace(' ', 'T')).toLocaleDateString(),
        condition: post.book_condition,
        price: post.price,
        }));
    } catch (error) {
        console.error('Error fetching posts:', error);
        alert('Failed to fetch posts. Please try again.');
    }
};

const addPost = async () => {
    try {
        const bookListResponse = await fetch('/api/v1/book/booklist');
        if (!bookListResponse.ok) {
        throw new Error('Failed to fetch book list');
        }

        const bookList = await bookListResponse.json();

        const selectedBook = bookList.find((book) => book.isbn === isbn.value);
        if (!selectedBook) {
        throw new Error('Book not found in the book list');
        }

        const book_id = selectedBook.book_id;

        const newPostData = {
        seller_user_id: currentUser.value.id,
        book_id: book_id,
        book_condition: newPost.value.condition,
        price: newPost.value.price,
        };

        console.log('Sending New Post Data:', newPostData);

        const postResponse = await fetch('/api/v1/post/add_post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPostData),
        });

        if (!postResponse.ok) {
        throw new Error('Failed to add post');
        }

        alert('Post added successfully!');
        fetchPosts(isbn.value);
        showAddPostModal.value = false;
    } catch (error) {
        console.error('Error adding post:', error);
        alert('Failed to add post. Please try again.');
    }
};

const replyToPost = (postId, sellerUserId) => {
    if (!currentUser.value || !currentUser.value.id) {
        alert('Please log in to reply.');
        return;
    }

    fetch(`/api/v1/reply/history?post_id=${encodeURIComponent(postId)}&seller_user_id=${encodeURIComponent(sellerUserId)}&buyer_user_id=${encodeURIComponent(currentUser.value.id)}`)
        .then((response) => {
        if (!response.ok) {
            throw new Error('Failed to fetch conversation history');
        }
        return response.json();
        })
        .then((data) => {
        currentConversation.value = data.reply_history || [];
        showReplyModal.value = true;
        })
        .catch((error) => {
        console.error('Error fetching conversation history:', error);
        currentConversation.value = [];
        showReplyModal.value = true;
        });
};

const sendReply = (postId, sellerUserId) => {
    if (!newMessageContent.value) {
        alert('Message cannot be empty.');
        return;
    }

    const replyData = {
        from_user_id: currentUser.value.id,
        to_user_id: sellerUserId,
        post_id: postId,
        message: newMessageContent.value,
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
        currentConversation.value.push({
            ...createdReply,
            reply_time: new Date().toISOString(),
        });
        newMessageContent.value = '';
        })
        .catch((error) => {
        console.error('Error sending reply:', error);
        alert('Failed to send reply. Please try again.');
        });
};

onMounted(() => {
    console.log('Received ISBN:', isbn.value);
    if (!isbn.value) {
        alert('ISBN is missing!');
        return;
    }

    fetchBookDetails(isbn.value);
    fetchPosts(isbn.value);
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

  <div v-if="showReplyModal" class="modal-overlay" @click.self="showReplyModㄗㄗal = false">
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
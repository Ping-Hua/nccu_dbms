<template>
  <div class="home">
    <div class="header">
      <div class="header-container">
        <h3 class="title">Book List</h3>
          <div class="search-bar">
          <input
          type="text"
          placeholder="Search for books"
          v-model="searchQuery"
            />
            <button @click="searchBooks" class="search-button">
              <img :src="searchIcon" alt="Search Icon" width="20" />
            </button>
          </div>
      </div>
      <hr />

      <div class="main-content">
        <div class="categories">
          <span
            class="category"
            :class="{ active: selectedGenre === null }"
            @click="filterBooks(null)"
          >
            All
          </span>
          <span
            v-for="genre in genres"
            v-if="genres.length > 0"
            :key="genre.genre_id"
            class="category"
            :class="{ active: selectedGenre === genre.genre_id }"
            @click="filterBooks(genre.genre_id)"
          >
            {{ genre.genre_name }}
          </span>
        </div>

        <button class="btn-add-book" @click="openISBNModal">+ Add Book</button>
      </div>
    </div>

    <div class="books-container">
      <div
        class="book-card"
        v-for="book in books"
        :key="book.bookId"
        @click="viewBookDetails(book.bookId)"
      >
        <img :src="book.BookPictureUrl" alt="Book Cover" class="book-cover" />
        <p><b>{{ book.BookName }}</b></p>
        <p>Author: {{ book.Author }}</p>
        <p>Public Year: {{ book.PublicYear }}</p>
      </div>
    </div>

    <div v-if="showConfirmModal" class="modal-overlay" @click.self="closeConfirmModal">
      <div class="modal-content">
        <h4>Confirm Book Details</h4>
        <div class="form-group">
          <label><b>Book Name:</b></label>
          <p>{{ bookToConfirm?.BookName || "Unknown" }}</p>
        </div>
        <div class="form-group">
          <label><b>Author:</b></label>
          <p>{{ bookToConfirm?.Author || "Unknown" }}</p>
        </div>
        <div class="form-group">
          <label><b>Publisher:</b></label>
          <p>{{ bookToConfirm?.Publisher || "Unknown" }}</p>
        </div>
        <div class="form-group">
          <label><b>Public Year:</b></label>
          <p>{{ bookToConfirm?.PublicYear || "Unknown" }}</p>
        </div>
        <div class="form-group">
          <label><b>ISBN:</b></label>
          <p>{{ bookToConfirm?.ISBN }}</p>
        </div>
        <div class="form-group">
          <label for="genre">Select Genre:</label>
          <select id="genre" v-model="manualBookDetails.genre" required>
            <option v-for="genre in genres" :key="genre.genre_id" :value="genre.genre_id">
              {{ genre.genre_name }}
            </option>
          </select>
        </div>
        <div class="button-group">
          <button @click="confirmBook" class="btn-submit">Confirm</button>
          <button @click="closeConfirmModal" class="btn-cancel">Cancel</button>
        </div>
      </div>
    </div>


    <div v-if="showISBNModal" class="modal-overlay" @click.self="closeISBNModal">
      <div class="modal-content">
        <h4>Add Book</h4>
        <form @submit.prevent="searchBookByISBN">
          <div class="form-group">
            <label for="isbn">ISBN:</label>
            <input 
              type="text" 
              inputmode="numeric" 
              v-model="isbn" 
              required 
              autocomplete="off" 
              placeholder="Enter ISBN" 
            />
          </div>
          <div class="button-group">
            <button type="submit" class="btn-add-book">Search</button>
            <button type="button" class="btn-cancel" @click="closeISBNModal">Cancel</button>
          </div>
        </form>
      </div>
    </div>


    <div v-if="showManualModal" class="modal-overlay" @click.self="showManualModal = false">
      <div class="modal-content">
        <h4>Enter Book Details</h4>
        <form @submit.prevent="addBookManually">
          <div class="form-group">
            <label for="bookName">Book Name:</label>
            <input type="text" id="bookName" v-model="manualBookDetails.name" required autocomplete="off" />
          </div>
          <div class="form-group">
            <label for="author">Author:</label>
            <input type="text" id="author" v-model="manualBookDetails.author" required autocomplete="off"/>
          </div>
          <div class="form-group">
            <label for="isbn">ISBN:</label>
            <input type="text" id="isbn" v-model="manualBookDetails.isbn" required autocomplete="off" />
          </div>
          <div class="form-group">
            <label for="publicYear">Public Year:</label>
            <input type="text" id="publicYear" v-model="manualBookDetails.publicYear" required autocomplete="off"/>
          </div>
          <div class="form-group">
            <label for="publisher">Publisher:</label>
            <input type="text" id="publisher" v-model="manualBookDetails.publisher" required autocomplete="off"/>
          </div>
          <div class="form-group">
            <label for="genre">Genre:</label>
            <select id="genre" v-model="manualBookDetails.genre" required>
              <option v-for="genre in genres" :key="genre.genre_id" :value="genre.genre_id">
                {{ genre.genre_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="bookPicture">Book Picture URL:</label>
            <input 
              type="text" 
              id="bookPicture" 
              v-model="manualBookDetails.bookPictureUrl" 
              required autocomplete="off"
              placeholder="Enter Image URL (e.g., https://example.com/image.jpg)" 
            />
          </div>
          <div class="button-group">
            <button type="submit" class="btn-submit">Submit</button>
            <button type="button" class="btn-cancel" @click="showManualModal = false">Cancel</button>
          </div>
        </form>
      </div>
</div>

  </div>
</template>


<script>
import searchIcon from "../assets/search_icon.png";
const API_BASE_URL = import.meta.env.VITE_BE_API_BASE_URL;

export default {
  data() {
    return {
      books: [], 
      genres: [], 
      selectedGenre: null, 
      showISBNModal: false,
      showManualModal: false,
      showConfirmModal: false,
      isbn: "", 
      searchQuery: "", 
      bookToConfirm: null,
      manualBookDetails: {
      name: '',
      author: '',
      isbn: '',
      publicYear: '',
      publisher: '',
      genre: '', 
      bookPictureUrl: '',
      },
      searchIcon,
    };
  },
  created() {
    this.fetchAllBooks();
    this.fetchGenres(); 
  },
  
  methods: {
  openISBNModal() {
    this.isbn = ""; 
    this.showISBNModal = true; 
  },
  closeISBNModal() {
    this.isbn = "";
    this.showISBNModal = false; 
  },


async fetchAllBooks() {
    try {
      const response = await fetch("/api/v1/book/booklist", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch books from the server.");
      }

      const data = await response.json();

      this.books = data.map((book) => ({
        ISBN: book.ISBN,
        BookName: book.book_name,
        Author: book.author,
        PublicYear: book.public_year,
        Publisher: book.publisher,
        BookPictureUrl: book.book_picture_url,
        Genre: book.genre_id,
        bookId: book.book_id,
      }));
    } catch (error) {
      console.error("Error fetching books:", error);
      alert("An error occurred while fetching the book list. Please try again.");
    }
  },

  viewBookDetails(bookId) {
  if (!bookId) {
    alert("Book ID is missing!");
    return;
  }

  this.$router.push({ name: "post", params: { bookId } });
},

async fetchGenres() {
  try {
    const response = await fetch('/api/v1/genre/genres', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch genres from the server.');
    }

    const data = await response.json();
    this.genres = data.map((genre) => ({
      genre_id: genre.genre_id,
      genre_name: genre.genre_name,
    }));
  } catch (error) {
    console.error('Error fetching genres:', error);
    alert('An error occurred while fetching the genres. Please try again.');
  }
},
    
async filterBooks(genreId) {
  this.selectedGenre = genreId;

  try {
    const url = genreId !== null
      ? `/api/v1/book/booklist?genre_id=${genreId}`
      : "/api/v1/book/booklist";

    console.log("Fetching books with URL:", url); 

    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch books.");
    }

    const data = await response.json();

    this.books = data.map((book) => ({
      ISBN: book.ISBN,
      BookName: book.book_name,
      Author: book.author,
      PublicYear: book.public_year || "Unknown", // 處理空值
      Publisher: book.publisher,
      BookPictureUrl: book.book_picture_url,
      Genre: book.genre_id,
    }));

    console.log("Filtered books:", this.books); // 測試輸出
  } catch (error) {
    console.error("Error filtering books:", error);
    alert("An error occurred while filtering books. Please try again.");
  }
},




async searchBooks() {
    try {
      if (!this.searchQuery || this.searchQuery.trim() === '') {
        alert('Please enter a book name to search.');
        return;
      }

      const response = await fetch(`/api/v1/book/search_books?query=${encodeURIComponent(this.searchQuery.trim())}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch book data');
      }

      const data = await response.json();

      if (data.success && data.book && data.book.length > 0) {
        this.books = data.book.map((book) => ({
          ISBN: book.ISBN,
          BookName: book.book_name,
          Author: book.author,
          PublicYear: book.public_year,
          Publisher: book.publisher,
          BookPictureUrl: book.book_picture_url
          ? `${API_BASE_URL}/${book.book_picture_url}` 
          : null, 
          Genre: book.genre_id 
        }));
        alert('Books fetched successfully!');
      } else {
        alert('No books found matching your query.');
      }
    } catch (error) {
      console.error('Error searching books:', error);
      alert('An error occurred while searching for books. Please try again.');
    }
  },


async searchBookByISBN() {
  try {
    const isbn = this.isbn.trim();

    if (!/^\d{13}$/.test(isbn)) {
      alert("Invalid ISBN. Please enter a valid 13-digit ISBN.");
      return;
    }

    const response = await fetch(`/api/v1/book/get_book_by_isbn?isbn=${isbn}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      if (response.status === 404) {
        alert("Book not found. Please enter details manually.");
        this.showManualModal = true; // 顯示手動輸入模態框
      } else {
        throw new Error("Failed to fetch book details.");
      }
      return;
    }

    const book = await response.json();
    this.bookToConfirm = {
      ISBN: book.ISBN,
      BookName: book.book_name,
      Author: book.author,
      PublicYear: book.public_year,
      Publisher: book.publisher,
      BookPictureUrl: book.book_picture_url,
    };
    this.showConfirmModal = true; // 顯示確認模態框
  } catch (error) {
    console.error("Error searching book by ISBN:", error);
    alert("An error occurred while searching for the book. Please try again.");
  } finally {
    this.showISBNModal = false; // 關閉 ISBN 搜尋模態框
  }
},

async confirmBook() {
  if (!this.selectedGenre) {
    alert("Please select a genre.");
    return;
  }

  try {
    const newBook = {
      ...this.bookToConfirm,
      genre_id: this.selectedGenre, // 添加分類 ID
    };

    const response = await fetch("/api/v1/book/add_book", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newBook),
    });

    if (!response.ok) {
      throw new Error("Failed to add book.");
    }

    const addedBook = await response.json();

    this.books.push({
      ISBN: addedBook.ISBN,
      BookName: addedBook.book_name,
      Author: addedBook.author,
      PublicYear: addedBook.public_year,
      Publisher: addedBook.publisher,
      BookPictureUrl: addedBook.book_picture_url,
      Genre: addedBook.genre_id, // 確保分類被正確設定
    });

    // 重新套用過濾邏輯
    this.filterBooks(this.selectedGenre);

    alert("Book added successfully!");
  } catch (error) {
    console.error("Error confirming book:", error);
    alert("An error occurred while confirming the book. Please try again.");
  } finally {
    this.closeConfirmModal();
  }
},


closeConfirmModal() {
  this.showConfirmModal = false;
  this.bookToConfirm = null;
  this.selectedGenre = null;
},



async addBookManually() {
    
    try {
      const existingBook = this.books.find(
      (book) => book.ISBN === this.manualBookDetails.isbn
    );
    if (existingBook) {
      alert('This book already exists');
      return;
    }

    const newBook = {
      ISBN: this.manualBookDetails.isbn,
      book_name: this.manualBookDetails.name,
      author: this.manualBookDetails.author,
      public_year: this.manualBookDetails.publicYear,
      publisher: this.manualBookDetails.publisher,
      book_picture_url: this.manualBookDetails.bookPictureUrl, 
      genre_id: this.manualBookDetails.genre
    };

    const response = await fetch('/api/v1/book/add_book', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newBook),
    });

    if (!response.ok) {
      throw new Error('Failed to add book');
    }

    const addedBook = await response.json();
    console.log('Books List:', this.books);

    this.books.push({
      ISBN: addedBook.ISBN,
      BookName: addedBook.book_name,
      Author: addedBook.author,
      PublicYear: addedBook.public_year,
      Publisher: addedBook.publisher,
      BookPictureUrl: addedBook.book_picture_url,
      Genre: addedBook.genre_id 
    });

    await this.filterBooks(this.selectedGenre);

    alert('Book added successfully!');
  } catch (error) {
    console.error('Error adding book:', error);
    alert('An error occurred while adding the book. Please try again.');
  } finally {
    this.manualBookDetails = {
      name: '',
      author: '',
      isbn: '',
      publicYear: '',
      publisher: '',
      genre: '',
      bookPictureUrl: ''
    };
    this.showManualModal = false;
  }
},
},
};

</script>


<style scoped>
.home {
  padding-top: 20px; 
}

body {
  margin: 0;
  padding: 20px;
}

.main-content {
  display: flex;
  justify-content: space-between; 
  align-items: center;
  margin-bottom: 20px;
}

.header {
  text-align: center;
  margin-bottom: 10px;
  margin-top: 20px; 
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

hr {
  border: 0;
  border-top: 1px solid #D0D0D0;
  margin: 10px 0;
}


.book-cover {
width: 150px;
height: 170px;
border-radius: 8px;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
object-fit: cover; /* 確保圖片不會變形 */
}

.categories {
  display: flex;
  gap: 20px; 
  margin-bottom: 20px;
}

.category {
  font-size: 16px;
  color: #555;
  cursor: pointer;
  position: relative; 
  padding: 5px 0;
  transition: color 0.3s ease;
}

.category:hover {
  color: #000;
}

.category.active {
  font-weight: bold;
  color: #000;
}

.category.active::after {
  content: "";
  position: absolute;
  bottom: -0.5px; 
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #000; 
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
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: 500px; /* 增加寬度 */
  max-height: 80vh; /* 設定最大高度 */
  overflow-y: auto; /* 內容超過時可滾動 */
}

.modal-content::-webkit-scrollbar {
  width: 8px; /* 滾動條寬度 */
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: #ccc; /* 滾動條顏色 */
  border-radius: 4px; /* 滾動條圓角 */
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background-color: #aaa; /* 滾動條滑過時的顏色 */
}

.modal-content h4 {
  margin-top: 0;
  text-align: center;
  color: #4a4747;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
  color: #4a4747;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.btn-cancel {
  background-color: #aaa;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-cancel:hover {
  background-color: #888;
}

.btn-add-book {
  margin-left: 30px;
}

.btn-add-book:hover {
  border-color: #555555cf; 
  background-color: #f0f0f0; 
}

.btn-submit:hover {
  border-color: #555555cf; 
  background-color: #f0f0f0; 
}

.header-container {
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 10px; 
}


.search-bar {
  display: flex;
  align-items: center;
  gap: 5px; 
  margin-left: 50px;
}

.search-bar input {
  padding: 5px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
  width: 170px; 
}

.search-bar button {
  color: white;
  border: none;
  width: 40px; 
  height: 40px; 
  border-radius: 50%;
  display: flex; 
  justify-content: center; 
  align-items: center;
  padding: 5px 10px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-bar button:hover {
  background-color: #aaa;
}

.books-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px; 
  justify-content: flex-start; 
  margin-bottom: 200px;
}


.book-card {
  width: 200px;
  text-align: center; 
  padding: 10px; 
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
  border-radius: 8px; /* 圓角 */
  background-color: #fff;
}


</style>
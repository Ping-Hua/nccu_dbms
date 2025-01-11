<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const apiUrl = import.meta.env.VITE_BE_API_BASE_URL; 

const posts = ref([]);
const totalCount = ref(-1);

const userID = 666;  // 測試用

const getPostList = async () => {
    console.log('Fetching post List for user:', userID);
    try {
        const { data } = await axios.get(`${apiUrl}/post/user_post`, {
            params: { user_id: userID },
        });

        if (data && Array.isArray(data.post_list)) {
            posts.value = data.post_list.map((post, index) => ({
                ...post,
                index: index + 1,
            }));
            totalCount.value = data.total_count;
            console.log("Post list fetched successfully:", posts.value);
        } else {
            posts.value = []; 
            totalCount.value = 0;
            console.log("No posts found for the user.");
        }
    } catch (error) {
        console.error("Error fetching post list:", error);
    }
};

onMounted(() => {
    getPostList();
});
</script>

<template>
    <div class="user-container-fluid d-flex flex-column m-0 py-0 px-1 px-sm-5 h-100 w-100" style="max-width:100vw">
        <!-- 個人資訊區 -->
        <h4 class="m-0 pt-3 pb-0 mb-2 ps-2">發文歷史紀錄</h4>
        <h5>User ID: {{ userID }}</h5>

        <!-- 賣的書區 -->
        <div 
            class="flex-fill px-2"
            style="overflow-y: scroll; max-height: calc(100vh - 185px)"
            ref="postHistoryContainer"
        >
            
            <div
                v-if="totalCount > 0"
                v-for="post in posts"
                :key="`post-${post.index}`"
                class="post-card w-100 my-2 d-flex align-items-center py-1 rounded"
            >   
                <div class="mx-3" style="width: 60px;">
                    <button 
                        class="btn btn-secondary btn-sm">修改
                    </button>
                </div>
                <div class="vr my-2"></div>
                <div class="mx-3" style="width: 60px;">
                    <button 
                        class="btn btn-secondary btn-sm">刪除
                    </button>
                </div>
                <div class="vr my-2"></div>
                <div class="w-100 mx-3" style="overflow: hidden">
                    <!-- post id -->
                    <div class="mt-1 mb-2 d-flex align-items-center gap-2">
                        <div class="fw-bold text-break">
                            {{ post.book_name }}
                        </div>

                        <div class="d-flex align-items-center justify-content-end gap-2 ms-auto">
                            書籍狀態：{{ post.book_condition }}
                        </div>
                    </div>
                    <!-- 價錢 -->
                    <div class="mt-1 mb-2 d-flex align-items-center gap-2">
                        <div class="fw-bold text-break">
                            Post ID: {{ post.post_id }}
                        </div>

                        <div class="d-flex align-items-center justify-content-end gap-2 ms-auto">
                            <span
                                class="badge rounded-pill bg-secondary"
                                style="font-size: 0.9rem;"
                            >
                                價錢
                            </span>
                            <span>{{ post.price }}元</span>
                        </div>
                    </div>
                </div>
                <div class="vr my-2"></div>
                <div class="mx-2 text-center" style="white-space: normal; word-break: keep-all; overflow-wrap: normal ;">
                    <small>
                        {{ new Date(post.create_time + 'Z').toLocaleString('zh-TW', {
                        timeZone: 'Asia/Taipei', 
                        month: '2-digit', 
                        day: '2-digit', 
                        hour: '2-digit', 
                        minute: '2-digit', 
                        hour12: true 
                    }) }}
                    </small>
                </div>
            </div>
            <!-- 無紀錄提示 -->
            <div 
                v-else 
                class="d-flex justify-content-center align-items-center"
                style="height: calc(100vh - 185px)"
            >
                <p class="text-muted text-center"> 您還沒發過文，歡迎使用 (⁎⁍̴̛ᴗ⁍̴̛⁎)</p>
            </div>
        </div>
    </div>
</template>


<style scoped>
.post-card {
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    border-radius: 8px;
    display: flex;
    align-items: center;
    color: #333;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.user-board {
  background-color: #f8f9fa;
  border-bottom: 2px solid #343a40;
}

.user-content {
  flex: 1; 
  overflow-y: auto; 
}
</style>
<script setup>
import { ref, defineProps, defineEmits } from "vue";
import axios from "axios";
import { useGlobalStore } from "../stores/global.js";

const globalStore = useGlobalStore();

const apiUrl = import.meta.env.VITE_BE_API_BASE_URL;

const emit = defineEmits(["updatePost", "close"]);

const props = defineProps({
    postId: {
        type: Number,
        required: true,
    },
    initialPrice: {
        type: Number,
        default: null,
    },
    initialBookCondition: {
        type: String,
        default: "",
    },
});

const price = ref(props.initialPrice);
const bookCondition = ref(props.initialBookCondition);

// ---- 更新 post API ----  
const updatePost = async (postId, updateFields) => {
    console.log('Updating post...');
    
    try {
        const payload = {
            post_id: postId,
            ...updateFields,
        };

        const { data } = await axios.put(`${apiUrl}/post/update_post`, payload);

        console.log("Post updated successfully.");
        return data;
    } catch (error) {
        console.error("Error updating post:", error);
        throw error;
    }
};

const handleSubmit = async () => {
    const updatedFields = {};

    if (price.value !== props.initialPrice) {
        updatedFields.price = parseFloat(price.value);
    }

    if (bookCondition.value !== props.initialBookCondition) {
        updatedFields.book_condition = bookCondition.value;
    }

    if (Object.keys(updatedFields).length === 0) {
        alert("請至少修改一個字段再提交！");
        return;
    }

    try {
        const response = await updatePost(props.postId, updatedFields);

        emit("updatePost", response);

        closeModal();
    } catch (error) {
        console.error("Error handling submit:", error);
        alert("更新失敗，請稍後再試一次。");
    }
};

const closeModal = () => {
  emit("close");
};
</script>

<template>
    <div class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <form @submit.prevent="handleSubmit">
                <label class="form-label title-label">修改貼文</label>

                <!-- Price Input -->
                <div class="row mb-3">
                    <label for="Price" class="form-label">價錢</label>
                    <input 
                        type="text" 
                        class="form-control" 
                        id="Price" 
                        v-model="price" 
                        placeholder="Update your price" 
                    />
                </div>

                <!-- Book Condition Input -->
                <div class="row mb-3">
                    <label for="BookCondition" class="form-label">書籍狀態</label>
                    <input 
                        type="text" 
                        class="form-control" 
                        id="BookCondition" 
                        v-model="bookCondition" 
                        placeholder="Update your book condition" 
                    />
                </div>

                <!-- Submit Button -->
                <button type="submit" class="btn btn-secondary">Submit</button>
            </form>
        </div>
    </div>
</template>

<style>
</style>

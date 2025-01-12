<script setup>
import { defineEmits, defineProps } from "vue";
import api from "../api/api.js";

const apiUrl = import.meta.env.VITE_BE_API_BASE_URL;

const props = defineProps({
    postId: {
        type: Number,
        required: true,
    },
});

const emit = defineEmits(["close", "postDeleted"]);

const deletePost = async () => {
    try {
        await api.delete(`${apiUrl}/post/delete_post/${props.postId}`);
        console.log(`Post with ID ${props.postId} deleted successfully.`);
        emit("postDeleted"); 
        closeModal();
    } catch (error) {
        console.error("Failed to delete post:", error);
        alert("刪除失敗，請稍後再試一次。");
    }
};

const closeModal = () => {
    emit("close");
};

</script>

<template>
    <div class="modal-overlay-deletepost" @click.self="closeModal">
        <div class="modal-content-deletepost">
            <p>確定要刪除嗎？</p>
            <div class="modal-buttons-deletepost">
                <button class="confirm btn btn-secondary" @click="deletePost">確定</button>
                <button class="cancel btn btn-secondary" @click="closeModal">取消</button>
            </div>
        </div>
    </div>
</template>

<style>
.modal-overlay-deletepost {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
}

.modal-content-deletepost {
  position: absolute;
  background: white;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 2rem;
  border-radius: 8px;
  width: 400px;
  height: 160px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-buttons-deletepost {
  display: flex;
  justify-content: center;
  gap: 2rem; 
}

.modal-buttons-deletepost button {
  width: 60px; 
  padding: 0.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
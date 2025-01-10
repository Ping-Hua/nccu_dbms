<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useGlobalStore } from '../stores/global.js';

const apiUrl = import.meta.env.VITE_BE_API_BASE_URL;
const globalStore = useGlobalStore();

const emits = defineEmits(['close', 'logout-success']);

// ---- 登出 ----
const logout = async () => {
    console.log('Logging out...');
    try {
        const { data } = await axios.post(`${apiUrl}/auth/logout`);
        console.log(data.message);

        globalStore.clearUser();
        alert("You have been logged out successfully.");

        emits('logout-success');
    } catch (error) {
        console.error('logout failed:', error.response?.data?.message);
        alert(error.response?.data?.message);
    } finally {
        closeModal();
    }
};

const closeModal = () => {
  emits('close'); // 觸發 close 事件
};
</script>

<template>
    <div class="modal-overlay-logout" @click.self="closeModal">
        <div class="modal-content-logout">
            <p>確定要登出嗎？</p>
            <div class="modal-buttons">
                <button class="confirm btn btn-secondary" @click="logout">確定</button>
                <button class="cancel btn btn-secondary" @click="closeModal">取消</button>
            </div>
        </div>
    </div>
</template>

<style>
.modal-overlay-logout {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
}

.modal-content-logout {
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

.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 2rem; 
}

.modal-buttons button {
  width: 60px; 
  padding: 0.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>

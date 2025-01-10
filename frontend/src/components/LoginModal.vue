<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api/api.js';
import { useGlobalStore } from '../stores/global.js';

const email = ref('');
const password = ref('');
const emits = defineEmits(['close']); 
const router = useRouter();
const apiUrl = import.meta.env.VITE_BE_API_BASE_URL;
const globalStore = useGlobalStore();


// ---- 按鈕 disable ----
const isLoginDisabled = computed(() => {
    return !email.value.trim() || !password.value.trim();
});

// ---- 登入 ----
const login = async () => {
    console.log("loaded with login");
    try {
        const payload = {
            email: email.value,
            password: password.value,
        };

        const { data } = await api.post(`${apiUrl}/auth/login` , payload);
        console.log("Login successfully");

        globalStore.setUser(data.id, data.name);
        return true;        
    } catch (error) {
        const errorMessage = error.response?.data?.messages || "An error occurred. Please try again.";
        console.error("Login failed:", errorMessage);
        alert(errorMessage);

        return false;
    }
};

const handleSubmit = async () => {
    const loginSuccess = await login(); // 登入功能
    
    if (loginSuccess) {
        // 清空 input-box
        email.value = ''; 
        password.value = '';

        emits('close'); // 提交後自動關閉 Modal
    }
};

const registerHandler = () => {
  emits('open-register') // 轉到註冊 modal
};

const closeModal = () => {
  emits('close'); // 觸發 close 事件
};
</script>

<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
        <form @submit.prevent="handleSubmit">
            <label class="form-label title-label">BookCycle</label>
            <div class="row mb-3">
                <input type="email" class="form-control" id="Email" v-model="email" placeholder="Email" />
            </div>
            <div class="row mb-3">
                <input type="password" class="form-control" id="Password" v-model="password" placeholder="Password" />
            </div>
            <button type="submit" class="btn btn-secondary" :disabled="isLoginDisabled">Login</button>

            <!-- Register Link -->
            <p class="register-link" data-bs-dismiss="modal" @click="registerHandler">Create new account</p>
         </form>
    </div>
  </div>
</template>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
}

.modal-content {
  position: absolute;
  background: white;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 2rem;
  border-radius: 8px;
  width: 400px;
  height: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.title-label {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  position: relative;
}

.title-label::before,
.title-label::after {
  content: "";
  flex: 1;
  height: 1px;
  background: #ccc;
  margin: 0 10px;
}

.register-link {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #6c757d;
  text-decoration: underline;
  text-align: center;
  cursor: pointer;
}

.register-link:hover {
  color: #5a6268;
  text-decoration: none;
}

</style>


<script setup>
import { ref, computed } from 'vue';
import api from '../api/api.js';
import { useRouter } from 'vue-router';

const apiUrl = import.meta.env.VITE_BE_API_BASE_URL;

const router = useRouter();

const email = ref('');
const password = ref('');
const username = ref('');
const studentNumber = ref('');
const phone = ref('');

const emits = defineEmits(['close', 'open-login']);

// 沒填完按鈕先禁用
const isRegisterDisabled = computed(() => {
    return (
        !email.value.trim() ||
        !password.value.trim() ||
        !username.value.trim() ||
        !studentNumber.value.trim() ||
        !phone.value.trim() 
    );
});

// ---- 註冊 ----
const register = async () => {
    console.log("Register new user");
    try {
        const payload = {
            email: email.value,
            password: password.value,
            user_name: username.value,
            student_number: studentNumber.value,
            phone: phone.value
        };

        const { data } = await api.post(`${apiUrl}/auth/register` , payload);
        console.log("Register successfully");
        return true;
    } catch (error) {
        console.error("Register failed:", error.response?.data?.messages);
        alert(error.response?.data?.messages || "Registration failed. Please try again.");
        return false;
    }
};

const handleSubmit = async () => {
    const registerSuccess = await register();
    
    if (registerSuccess){
        // 清空
        email.value = '';
        password.value = '';
        username.value = '';
        studentNumber.value = '';
        phone.value = '';

        emits('close');
        emits('open-login');
    }
};

const closeModal = () => {
  emits('close'); // 觸發 close 事件
};
</script>

<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
        <form class="row g-3" @submit.prevent="handleSubmit">
            <label class="form-label title-label">Register</label>
            <div class="mb-2">
                <input type="email" class="form-control" id="email" v-model="email" placeholder="Email">
            </div>
            <div class="mb-2">
                <input type="password" class="form-control" id="password" v-model="password" placeholder="Password">
            </div>
            <div class="col-md-6">
                <input type="text" class="form-control" id="student-number" v-model="studentNumber" placeholder="Student Number">
            </div>
            <div class="col-md-6">
                <input type="text" class="form-control" id="phone" v-model="phone" placeholder="Phone">
            </div>
            <div class="mb-2">
                <input type="username" class="form-control" id="username" v-model="username" placeholder="User Name">
            </div>
            <button type="submit" class="btn btn-secondary" id="register-btn" :disabled="isRegisterDisabled">Register</button>
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
  z-index: 10000; 
}

.modal-content {
  position: absolute;
  background: white;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 2rem;
  border-radius: 8px;
  width: 500px;
  height: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 10001; 
}

.title-label {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
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

#register-btn {
  margin-top: 1.5rem;
}
</style>
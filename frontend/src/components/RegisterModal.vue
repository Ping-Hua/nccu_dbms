<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const apiUrl = import.meta.env.VITE_BE_API_BASE_URL;

const router = useRouter();

const email = ref('');
const password = ref('');
const username = ref('');
const studentNumber = ref('');
const phone = ref('');

const emits = defineEmits(['close', 'open-login']);

// ---- 註冊 ----
const Register = async () => {
    console.log("Register new user");
    try {
        const payload = {
            email: email.value,
            password: password.value,
            user_name: username.value,
            student_number: studentNumber.value,
            phone: phone.value
        };

        const { data } = await axios.post(`${apiUrl}/auth/register` , payload);
        console.log("Register successfully");
    } catch (error) {
        console.error("Register failed:", error.message);
    }
};

const handleSubmit = async () => {
    
    if (!email.value.trim() || !password.value.trim()) {
        alert('Email and Password are required.');
        return;
    }

    if (!studentNumber.value || studentNumber.value.length !== 9) {
        alert('Please enter a valid student number.');
        return;
    }

    if (!username.value.trim()) {
        alert('User Name is required.');
        return;
    }

    if (!phone.value || phone.value.length !== 10) {
        alert('Please enter a valid phone number.');
        return;
    }

    try {
        await Register();

        // 清空
        email.value = '';
        password.value = '';
        username.value = '';
        studentNumber.value = '';
        phone.value = '';

        emits('close');
        emits('open-login');
    } catch (error) {
        console.error("Register failed:", error.message);
        alert("Registration failed. Please try again.");
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
            <button type="submit" class="btn btn-secondary" id="register-btn">Register</button>
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
  width: 500px;
  height: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
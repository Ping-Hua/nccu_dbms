<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const emits = defineEmits(['close']); 

const router = useRouter();

const handleSubmit = () => {
  console.log(`Email: ${email.value}, Password: ${password.value}`);
  email.value = ''; // 清空 email 輸入框
  password.value = ''; // 清空 password 輸入框
  emits('close'); // 提交後自動關閉 Modal
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
            <button type="submit" class="btn btn-secondary">Login</button>

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


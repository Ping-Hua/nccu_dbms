import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useGlobalStore = defineStore('global', () => {
    const user = ref({
        id: '',
        email: '',
    });

    const loginStatus = ref('default'); // 'default', 'logged_in', 'logged_out'
    
    const showLoginModal = ref(false);

    const setUser = (id, email) => {
        user.value = { id, email };
        loginStatus.value = 'logged_in';
    };

    const clearUser = () => {
        user.value = { id: '', email: '' };
        loginStatus.value = 'logged_out';
    };

    const toggleLoginModal = (status) => {
        showLoginModal.value = status;
    };

    return { user, loginStatus, showLoginModal, setUser, clearUser, toggleLoginModal };
}, {
    persist: {
        enabled: true,
        strategies: [
            {
                key: 'global_store',
                storage: localStorage,
                paths: ['user', 'loginStatus'],
            },
        ],
    },
});
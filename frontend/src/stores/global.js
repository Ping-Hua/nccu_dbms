import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useGlobalStore = defineStore('global', () => {
    const user = ref({
        id: '',
        name: '',
    });

    const loginStatus = ref('default'); // 'default', 'logged_in', 'logged_out'

    const setUser = (id, name) => {
        user.value = { id, name };
        loginStatus.value = 'logged_in';
    };

    const clearUser = () => {
        user.value = { id: '', name: '' };
        loginStatus.value = 'logged_out';
    };

    return { user, loginStatus, setUser, clearUser };
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
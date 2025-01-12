import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import { useGlobalStore } from '../stores/global.js';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/user',
            name: 'user',
            component: () => import('../views/UserView.vue'),
            meta: { requireAuth: 'true' },
        },
        {
            path: '/',
            name: 'book',
            component: () => import('../views/BookView.vue')
        },
        {
            path: '/post/:bookId',
            name: 'post',
            component: () => import('../views/PostView.vue'),
            meta: { requireAuth: 'true' },
        },
        {
            path: '/comments',
            name: 'comments',
            component: () => import('../views/CommentView.vue'),
            meta: { requireAuth: 'true' },
        }
    ],
});

router.beforeEach((to, from, next) => {
    const globalStore = useGlobalStore();

    if (to.meta.requireAuth) {
        if (globalStore.loginStatus === 'logged_in') {
            next();
        } else {
            globalStore.toggleLoginModal(true);
            next(false);
        }
    } else {
        next();
    }
});



export default router;

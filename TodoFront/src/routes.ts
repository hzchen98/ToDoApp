import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/start',
        name: 'start-layout',
        component: () => import('./layouts/IndexLayout.vue'),
        children: [
            {
                path: '',
                name: 'start-page',
                component: () => import('./pages/IndexPage.vue'),
            },]
    },
    {
        path: '/',
        name: 'main',
        redirect: '/start',
        component: () => import('./layouts/MainLayout.vue'),
        children: [
            {
                path: '',
                name: 'home',
                component: () => import('./pages/HomePage.vue'),
            },
            { path: "/:pathMatch(.*)*", redirect: '/start' }
        ]
    }

]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})


export default router

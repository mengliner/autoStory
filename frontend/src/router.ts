import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'projects',
      component: () => import('./views/ProjectListPage.vue')
    },
    {
      path: '/story/:id',
      name: 'story',
      component: () => import('./views/StoryPage.vue')
    },
    {
      path: '/story/:id/preview',
      name: 'preview',
      component: () => import('./views/PreviewPage.vue')
    }
  ]
})

export default router

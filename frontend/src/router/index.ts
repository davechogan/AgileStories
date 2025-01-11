import { createRouter, createWebHistory } from 'vue-router'
import StoryInput from '@/views/StoryInput.vue'
import TestFormatView from '@/views/TestFormatView.vue'
import TestTechReviewView from '@/views/TestTechReviewView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: StoryInput
    },
    {
      path: '/test-format',
      name: 'test-format',
      component: TestFormatView
    },
    {
      path: '/test-tech-review',
      name: 'test-tech-review',
      component: TestTechReviewView
    }
  ]
})

export default router

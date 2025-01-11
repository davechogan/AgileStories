import { createRouter, createWebHistory } from 'vue-router'
import StoryInput from '@/views/StoryInput.vue'
import TestFormatView from '@/views/TestFormatView.vue'
import AgileReview from '@/views/AgileReview.vue'
import TechReview from '@/views/TechReview.vue'
import TestTechReviewView from '@/views/TestTechReviewView.vue'
import TestEstimateView from '@/views/TestEstimateView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: StoryInput
    },
    {
      path: '/test/story',
      name: 'test-story',
      component: TestFormatView
    },
    {
      path: '/test/agile',
      name: 'test-agile',
      component: AgileReview
    },
    {
      path: '/test/tech',
      name: 'test-tech',
      component: TechReview
    },
    {
      path: '/test/techreview',
      name: 'test-tech-review',
      component: TestTechReviewView
    },
    {
      path: '/test/estimate',
      name: 'test-estimate',
      component: TestEstimateView
    }
  ]
})

export default router

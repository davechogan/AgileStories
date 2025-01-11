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
      path: '/story',
      name: 'story',
      component: TestFormatView
    },
    {
      path: '/agile',
      name: 'agile',
      component: AgileReview
    },
    {
      path: '/tech',
      name: 'tech',
      component: TechReview
    },
    {
      path: '/techreview',
      name: 'tech-review',
      component: TestTechReviewView
    },
    {
      path: '/estimate',
      name: 'estimate',
      component: TestEstimateView
    }
  ]
})

export default router

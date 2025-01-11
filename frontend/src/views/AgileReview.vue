<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column: Primary Content -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <div class="story-section">
            <h3>Improved Story</h3>
            <div class="editable-content">
              <pre>{{ analysis.improved_story.text }}</pre>
            </div>
            
            <h3>Enhanced Acceptance Criteria</h3>
            <div class="editable-content">
              <ul>
                <li v-for="(criterion, index) in analysis.improved_story.acceptance_criteria" 
                    :key="index">
                  {{ criterion }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <!-- Sticky footer inside primary-content-wrapper -->
        <div class="sticky-footer">
          <div class="footer-content">
            <v-btn 
              color="primary" 
              @click="router.push('/tech')"
            >
              Continue to Tech Review
            </v-btn>
          </div>
        </div>
      </div>

      <!-- Right Column: Analysis Panel -->
      <div class="analysis-panel">
        <div class="analysis">
          <h3>Analysis</h3>
          <div class="invest-grid">
            <div v-for="(item, index) in analysis.invest_analysis" :key="index" 
                 class="invest-item"
                 :class="{ 'warning': isNegative(item.content) }">
              <div class="invest-header">
                <span class="invest-letter">{{ item.letter }}</span>
                <span class="invest-title">{{ item.title }}</span>
              </div>
              <div class="invest-content">{{ item.content }}</div>
            </div>
          </div>
        </div>

        <div class="suggestions mt-6">
          <h3>Suggestions</h3>
          <div class="suggestions-list">
            <div v-for="(suggestion, key) in analysis.suggestions" 
                 :key="key"
                 class="suggestion-item">
              <div class="suggestion-header">{{ key }}</div>
              <div class="suggestion-content">{{ suggestion }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStoryStore } from '@/stores/storyStore'

const router = useRouter()
const storyStore = useStoryStore()

onMounted(() => {
  if (!storyStore.currentAnalysis) {
    router.push('/')
    return
  }
})

const analysis = computed(() => storyStore.currentAnalysis)

// Add this function to detect negative feedback
const isNegative = (content: string): boolean => {
  const negativeTerms = ['not', 'too vague', 'unclear', 'missing'];
  return negativeTerms.some(term => content.toLowerCase().includes(term));
}
</script>

<style>
/* Copy all styles exactly from TestFormatView.vue */
.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
  min-height: 100vh;
  position: relative;
}

/* ... rest of styles from TestFormatView.vue ... */
</style> 
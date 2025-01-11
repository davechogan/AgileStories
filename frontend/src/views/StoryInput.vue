<template>
  <div class="story-input">
    <h2>User Story Input</h2>
    
    <div class="input-section">
      <label>Story:</label>
      <textarea 
        v-model="story.text"
        placeholder="As a [user type], I want [goal], so that [benefit]"
        rows="3"
      />
    </div>
    
    <div class="input-section">
      <label>Acceptance Criteria:</label>
      <div 
        v-for="(criteria, index) in story.acceptance_criteria" 
        :key="index"
        class="criteria-row"
      >
        <input 
          v-model="story.acceptance_criteria[index]"
          placeholder="Enter acceptance criteria"
        />
        <button @click="removeCriteria(index)" class="remove-btn">
          Remove
        </button>
      </div>
      <button @click="addCriteria" class="add-btn">
        Add Criteria
      </button>
    </div>
    
    <div class="input-section">
      <label>Context:</label>
      <textarea 
        v-model="story.context"
        placeholder="Add any additional context or background information"
        rows="2"
      />
    </div>
    
    <div class="error" v-if="error">{{ error }}</div>
    
    <v-btn
      color="primary"
      :loading="loading"
      :disabled="!story.text || story.acceptance_criteria.length === 0"
      @click="submitStory"
      class="submit-btn"
    >
      Submit for Analysis
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStoryStore } from '@/stores/storyStore'
import { submitStoryForAgileReview } from '@/api/storyApi'
import type { Story } from '@/types'

const router = useRouter()
const storyStore = useStoryStore()
const loading = ref(false)
const error = ref('')

const story = ref<Story>({
  text: '',
  acceptance_criteria: [''],
  context: ''
})

const submitStory = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const result = await submitStoryForAgileReview(story.value)
    storyStore.setAnalysis(result)  // Store the result
    router.push('/agile')
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'An error occurred'
    console.error('Error submitting story:', e)
  } finally {
    loading.value = false
  }
}

// Helper to add/remove acceptance criteria
const addCriteria = () => {
  story.value.acceptance_criteria.push('')
}

const removeCriteria = (index: number) => {
  story.value.acceptance_criteria.splice(index, 1)
}
</script>

<style scoped>
.story-input {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.input-section {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

textarea, input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.2);
  color: white;
}

.criteria-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.error {
  color: #ff5252;
  margin-bottom: 1rem;
}

.submit-btn {
  width: 100%;
}
</style> 
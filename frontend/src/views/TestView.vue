<template>
  <div class="test">
    <h1>Test Page</h1>
    <div class="story-generator">
      <textarea 
        v-model="storyInput"
        placeholder="Describe what you want your user story to be about..."
        rows="4"
      ></textarea>
      <button 
        @click="generateStory"
        :disabled="isProcessing"
      >
        {{ isProcessing ? 'Processing...' : 'Generate Story' }}
      </button>
      
      <div v-if="generatedStory" class="story-output">
        <h3>Generated Story:</h3>
        <pre>{{ generatedStory }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const storyInput = ref('')
const generatedStory = ref('')
const isProcessing = ref(false)

const generateStory = async () => {
  if (!storyInput.value.trim()) return
  
  isProcessing.value = true
  try {
    // TODO: Replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    generatedStory.value = `As a user\nI want to ${storyInput.value}\nSo that I can improve my workflow`
  } catch (error) {
    console.error('Error generating story:', error)
  } finally {
    isProcessing.value = false
  }
}
</script>

<style scoped>
.test {
  padding: 20px;
}

.story-generator {
  max-width: 600px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

textarea {
  width: 100%;
  padding: 8px;
}

button {
  padding: 8px 16px;
  cursor: pointer;
}

.story-output {
  margin-top: 20px;
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 4px;
}
</style> 
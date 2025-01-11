<template>
  <div class="test-view">
    <h1>Story Analysis Test</h1>
    
    <StoryInput @analysis-complete="handleAnalysis" />
    
    <!-- Debug output -->
    <v-card v-if="lastAnalysis" class="mt-4">
      <v-card-title>Analysis Results</v-card-title>
      <v-card-text>
        <pre>{{ JSON.stringify(lastAnalysis, null, 2) }}</pre>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import StoryInput from '@/components/story/StoryInput.vue'
import type { StoryAnalysis } from '@/types/story'

const lastAnalysis = ref<StoryAnalysis | null>(null)

const handleAnalysis = (analysis: StoryAnalysis) => {
  lastAnalysis.value = analysis
  console.log('Received analysis:', analysis)
}
</script>

<style scoped>
.test-view {
  padding: 2rem;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style> 
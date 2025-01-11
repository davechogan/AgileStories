<template>
  <div class="test">
    <h1>Story Generator</h1>
    
    <!-- Input Form -->
    <div v-if="currentStep === 'input'" class="story-form">
      <div class="form-section">
        <h2>1. User Story</h2>
        <p class="hint">Describe what you want to achieve. You can use the format: As a [role] I want to [action] so that [benefit]</p>
        <textarea 
          v-model="storyInput"
          placeholder="Example: As a user, I want to reset my password..."
          rows="4"
        ></textarea>
      </div>

      <div class="form-section">
        <h2>2. Acceptance Criteria</h2>
        <p class="hint">List the conditions that must be met for the story to be considered complete</p>
        <div class="criteria-list">
          <div v-for="(criterion, index) in acceptanceCriteria" :key="index" class="criteria-item">
            <input 
              v-model="acceptanceCriteria[index]"
              placeholder="Enter a criterion"
            >
            <button @click="removeCriterion(index)" class="remove-btn">×</button>
          </div>
          <button @click="addCriterion" class="add-btn">+ Add Criterion</button>
        </div>
      </div>

      <div class="form-section">
        <h2>3. Additional Context</h2>
        <p class="hint">Add any background information or constraints that might be relevant</p>
        <textarea 
          v-model="contextInput"
          placeholder="Example: This is part of our security compliance initiative..."
          rows="3"
        ></textarea>
      </div>

      <button 
        @click="startAnalysis"
        :disabled="isProcessing || !isValidInput"
        class="submit-btn"
      >
        {{ isProcessing ? 'Processing...' : 'Start Analysis' }}
      </button>
    </div>

    <!-- Agile Coach Review -->
    <div v-if="currentStep === 'agileCoachReview'" class="workflow-step">
      <h2>Agile Coach Review</h2>
      <div v-if="currentAnalysis" class="story-output">
        <div v-if="currentAnalysis.improved_story" class="improved-story">
          <h3>Improved Story:</h3>
          <pre>{{ currentAnalysis.improved_story.text }}</pre>
          
          <h3>Enhanced Acceptance Criteria:</h3>
          <ul>
            <li v-for="(criterion, index) in currentAnalysis.improved_story.acceptance_criteria" 
                :key="index">
              {{ criterion }}
            </li>
          </ul>
        </div>
        
        <div class="analysis">
          <h3>Analysis:</h3>
          <pre>{{ currentAnalysis.analysis }}</pre>
        </div>

        <div v-if="currentAnalysis.suggestions" class="suggestions">
          <h3>Suggestions:</h3>
          <ul>
            <li v-for="(suggestion, key) in currentAnalysis.suggestions" 
                :key="key">
              <strong>{{ key }}:</strong> {{ suggestion }}
            </li>
          </ul>
        </div>
      </div>
      
      <div class="action-buttons">
        <button @click="rejectAnalysis" :disabled="isProcessing">Reject & Edit</button>
        <button @click="approveAnalysis" :disabled="isProcessing">Accept & Continue</button>
      </div>
    </div>

    <!-- Technical Review -->
    <div v-if="currentStep === 'technicalReview'" class="workflow-step">
      <h2>Technical Review</h2>
      <div v-if="currentAnalysis" class="story-output">
        <div class="analysis">
          <h3>Technical Analysis:</h3>
          <pre>{{ currentAnalysis.analysis }}</pre>
        </div>
        
        <div v-if="currentAnalysis.suggestions" class="suggestions">
          <h3>Technical Suggestions:</h3>
          <ul>
            <li v-for="(suggestion, key) in currentAnalysis.suggestions" 
                :key="key">
              <strong>{{ key }}:</strong> {{ suggestion }}
            </li>
          </ul>
        </div>

        <div class="improved-story">
          <h3>Final Story:</h3>
          <pre>{{ currentAnalysis.improved_story?.text }}</pre>
          
          <h3>Final Acceptance Criteria:</h3>
          <ul>
            <li v-for="(criterion, index) in currentAnalysis.improved_story?.acceptance_criteria" 
                :key="index">
              {{ criterion }}
            </li>
          </ul>
        </div>
      </div>
      
      <div class="action-buttons">
        <button @click="rejectAnalysis" :disabled="isProcessing">Reject & Edit</button>
        <button @click="approveAnalysis" :disabled="isProcessing">Accept & Complete</button>
      </div>
    </div>

    <!-- Debug Section -->
    <div class="debug-section">
      <button @click="showDebug = !showDebug" class="debug-toggle">
        {{ showDebug ? 'Hide' : 'Show' }} Debug Info
      </button>
      <div v-if="showDebug" class="debug-output">
        <h3>Current Status: {{ currentAnalysis?.status || 'No analysis' }}</h3>
        <h3>Raw Response:</h3>
        <pre>{{ debugOutput }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Story {
  text: string;
  acceptance_criteria: string[];
  context: string;
  version: number;
}

interface AnalysisResult {
  original_story: Story;
  improved_story: Story | null;
  analysis: string;
  suggestions: Record<string, string>;
  status: string;
  timestamp: string;
}

const currentStep = ref('input')
const storyInput = ref('')
const acceptanceCriteria = ref([''])
const contextInput = ref('')
const isProcessing = ref(false)
const currentAnalysis = ref<AnalysisResult | null>(null)
const showDebug = ref(false)
const debugOutput = ref('')

const API_BASE_URL = 'http://localhost:8000'

const isValidInput = computed(() => {
  return storyInput.value.trim().length > 0 &&
         acceptanceCriteria.value.some(ac => ac.trim().length > 0)
})

const addCriterion = () => {
  acceptanceCriteria.value.push('')
}

const removeCriterion = (index: number) => {
  acceptanceCriteria.value = acceptanceCriteria.value.filter((_, i) => i !== index)
  if (acceptanceCriteria.value.length === 0) {
    acceptanceCriteria.value = ['']
  }
}

const startAnalysis = async () => {
  if (!isValidInput.value) return
  
  isProcessing.value = true
  try {
    const story: Story = {
      text: storyInput.value,
      acceptance_criteria: acceptanceCriteria.value.filter(ac => ac.trim()),
      context: contextInput.value,
      version: 1
    }

    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(story)
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`)
    }

    const result = await response.json()
    debugOutput.value = JSON.stringify(result, null, 2)
    currentAnalysis.value = result
    currentStep.value = 'agileCoachReview'
  } catch (error) {
    console.error('Analysis error:', error)
    debugOutput.value = `Error: ${error.message}`
  } finally {
    isProcessing.value = false
  }
}

const rejectAnalysis = async () => {
  if (!currentAnalysis.value) return
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        analysis_result: currentAnalysis.value,
        approved: false
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      console.error('Feedback API Error:', errorData)
      throw new Error(`API Error: ${response.status}`)
    }

    currentStep.value = 'input'
  } catch (error) {
    console.error('Feedback error:', error)
    debugOutput.value = `Error: ${error.message}`
  }
}

const approveAnalysis = async () => {
  if (!currentAnalysis.value) return
  
  try {
    const requestBody = {
      analysis_result: currentAnalysis.value,
      approved: true
    }
    
    console.log('Sending feedback - Full request body:', JSON.stringify(requestBody, null, 2))

    const response = await fetch(`${API_BASE_URL}/api/analyze/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody)
    })

    if (!response.ok) {
      const errorData = await response.json()
      console.error('Feedback API Error - Full details:', {
        status: response.status,
        data: errorData,
        sentData: requestBody
      })
      throw new Error(`API Error: ${response.status}`)
    }

    const result = await response.json()
    currentAnalysis.value = result
    if (result.status === 'technical_review') {
      currentStep.value = 'technicalReview'
    } else if (result.status === 'complete') {
      currentStep.value = 'complete'
    }
  } catch (error) {
    console.error('Feedback error:', error)
    debugOutput.value = `Error: ${error.message}`
  }
}
</script>

<style scoped>
.test {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  color: #333;
}

.story-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 8px;
}

.hint {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

textarea, input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  background-color: white;
  color: #333;
}

.criteria-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.criteria-item {
  display: flex;
  gap: 0.5rem;
}

.remove-btn {
  padding: 0 10px;
  background: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-btn {
  margin-top: 0.5rem;
  padding: 8px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn {
  padding: 12px 24px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1rem;
  margin-top: 1rem;
}

.submit-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.workflow-step {
  margin: 20px 0;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
}

.story-output {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  margin: 10px 0;
  color: #333;
}

.story-output.final {
  border: 2px solid #4CAF50;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #333;
}

h1, h2 {
  color: #333;
}

.action-buttons button {
  padding: 8px 16px;
  margin: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #2196F3;
  color: white;
}

.debug-section {
  margin-top: 2rem;
  padding: 1rem;
  border-top: 1px solid #ddd;
}

.debug-toggle {
  background: #666;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.debug-output {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.debug-output pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: monospace;
  font-size: 0.9rem;
  color: #333;
  background: #fff;
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #eee;
}

.debug-output h3 {
  margin-top: 0;
  color: #666;
  font-size: 1rem;
}

.improved-story, .analysis, .suggestions {
  margin-bottom: 1.5rem;
}

.improved-story h3, .analysis h3, .suggestions h3 {
  color: #2196F3;
  margin-bottom: 0.5rem;
}

.suggestions ul {
  list-style-type: none;
  padding-left: 0;
}

.suggestions li {
  margin-bottom: 0.5rem;
}

.suggestions strong {
  color: #666;
}

.analysis h3, .suggestions h3, .improved-story h3 {
  color: #2196F3;
  margin-bottom: 0.5rem;
}

.suggestions ul {
  list-style-type: none;
  padding-left: 0;
}

.suggestions li {
  margin-bottom: 0.5rem;
}

.suggestions strong {
  color: #666;
}

.action-buttons {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.action-buttons button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #2196F3;
  color: white;
}

.action-buttons button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background: white;
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #eee;
}
</style> 
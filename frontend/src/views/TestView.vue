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

    <!-- Review Tabs - Show when not in input step -->
    <div v-if="currentStep !== 'input'" class="review-tabs">
      <div class="tab-buttons">
        <button 
          @click="activeTab = 'agileCoach'"
          :class="{ active: activeTab === 'agileCoach' }"
          :disabled="currentStep === 'input'"
        >
          Agile Coach Review
        </button>
        <button 
          @click="activeTab = 'technical'"
          :class="{ active: activeTab === 'technical' }"
          :disabled="currentStep === 'input' || currentStep === 'agileCoachReview'"
        >
          Technical Review
        </button>
        <button 
          @click="activeTab = 'estimation'"
          :class="{ active: activeTab === 'estimation' }"
          :disabled="currentStep === 'input' || currentStep === 'agileCoachReview' || currentStep === 'technicalReview'"
        >
          Team Estimation
        </button>
      </div>

      <!-- Agile Coach Tab -->
      <div v-show="activeTab === 'agileCoach'" class="tab-content">
        <div class="workflow-step">
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
      </div>

      <!-- Technical Review Tab -->
      <div v-show="activeTab === 'technical'" class="tab-content">
        <div class="workflow-step">
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

interface TeamMember {
  id: number;
  name: string;
  title: string;
  initials: string;
  color: string;
  estimate: number;
  justification: string;
}

const currentStep = ref('input')
const storyInput = ref('')
const acceptanceCriteria = ref([''])
const contextInput = ref('')
const isProcessing = ref(false)
const currentAnalysis = ref<AnalysisResult | null>(null)
const activeTab = ref('agileCoach')
const teamEstimates = ref<TeamMember[]>([])

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
    currentAnalysis.value = result
    currentStep.value = 'agileCoachReview'
  } catch (error) {
    console.error('Analysis error:', error)
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
  }
}

const approveAnalysis = async () => {
  if (!currentAnalysis.value) return
  
  try {
    if (currentStep.value === 'technicalReview') {
      // Send to team for day estimation
      const response = await fetch(`${API_BASE_URL}/api/estimate/days`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          story: currentAnalysis.value.improved_story
        })
      })

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`)
      }

      const estimationResult = await response.json()
      processTeamEstimates(estimationResult)
      
      // Update UI state
      currentStep.value = 'estimation'
      activeTab.value = 'estimation'
    } else {
      // Handle other approval steps
      const response = await fetch(`${API_BASE_URL}/api/analyze/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          analysis_result: currentAnalysis.value,
          approved: true
        })
      })

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`)
      }

      const result = await response.json()
      currentAnalysis.value = result
      
      if (result.status === 'technical_review') {
        currentStep.value = 'technicalReview'
        activeTab.value = 'technical'
      }
    }
  } catch (error) {
    console.error('Analysis error:', error)
  }
}

const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const getRandomColor = (): string => {
  const colors = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
    '#D4A5A5', '#7FB069', '#E6B89C', '#9B7EDE'
  ]
  return colors[Math.floor(Math.random() * colors.length)]
}

const getPositionStyle = (index: number, total: number) => {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2 // Start from top
  const radius = 180 // Increased radius for 8 people
  const x = Math.cos(angle) * radius
  const y = Math.sin(angle) * radius
  return {
    transform: `translate(${x}px, ${y}px)`
  }
}

const processTeamEstimates = (estimationData: any) => {
  teamEstimates.value = estimationData.team_estimates.map((member: any, index: number) => ({
    id: index + 1,
    name: member.name,
    title: member.role,
    initials: getInitials(member.name),
    color: getRandomColor(),
    estimate: member.estimate,
    justification: member.justification
  }))
}

const circleStyles = {
  width: '500px',
  height: '500px'
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

.review-tabs {
  margin-top: 2rem;
}

.tab-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.5rem;
}

.tab-buttons button {
  padding: 0.5rem 1rem;
  border: none;
  background: none;
  color: #666;
  cursor: pointer;
  font-size: 1rem;
  position: relative;
}

.tab-buttons button.active {
  color: #2196F3;
  font-weight: bold;
}

.tab-buttons button.active::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  right: 0;
  height: 2px;
  background: #2196F3;
}

.tab-buttons button:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.tab-content {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.estimation-circle {
  position: relative;
  margin: 3rem auto;  /* Increased margin */
  border: 2px dashed #eee;
  border-radius: 50%;
}

/* Add title display */
.member-title {
  font-size: 0.7rem;
  color: #888;
  margin-top: 0.2rem;
}
</style> 
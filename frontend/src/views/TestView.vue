<template>
  <div class="test">
    <h1 class="story-generator-title">Story Generator</h1>
    
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

      <v-window v-model="activeTab">
        <!-- Agile Coach Tab -->
        <v-window-item value="agileCoach">
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
                <h3>Analysis</h3>
                <pre>{{ formatAnalysis(currentAnalysis?.analysis) }}</pre>
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
        </v-window-item>

        <!-- Technical Review Tab -->
        <v-window-item value="technical">
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
        </v-window-item>

        <!-- Team Estimation Tab -->
        <v-window-item value="estimation">
          <div v-if="teamEstimates && teamEstimates.length > 0">
            <h3>Team Estimates</h3>
            
            <!-- Circle layout with centered average -->
            <div class="estimation-circle" :style="circleStyles">
              <!-- Center average -->
              <div class="average-estimate">
                <div class="average-number">{{ averageEstimate }}</div>
                <div class="average-label">days average</div>
              </div>
              
              <!-- Team members -->
              <div 
                v-for="(member, index) in teamEstimates" 
                :key="member.name"
                class="team-member"
                :style="getPositionStyle(index, teamEstimates.length)"
              >
                <v-avatar
                  size="60"
                  :color="member.color"
                  class="member-avatar"
                  @click="showMemberDetails(member)"
                >
                  <span class="text-h6 white--text">{{ member.initials }}</span>
                </v-avatar>
                <div class="member-info">
                  <div class="member-name">{{ member.name }}</div>
                  <div class="member-title">{{ member.title }}</div>
                  <div class="member-estimate">{{ member.estimate }} days</div>
                </div>
              </div>
            </div>

            <!-- Member Details Modal -->
            <v-dialog v-model="showModal" max-width="500">
              <v-card v-if="selectedMember">
                <v-card-title class="d-flex align-center">
                  <v-avatar size="40" :color="selectedMember.color" class="mr-3">
                    <span class="text-h6 white--text">{{ selectedMember.initials }}</span>
                  </v-avatar>
                  {{ selectedMember.name }}
                </v-card-title>
                <v-card-subtitle>{{ selectedMember.title }}</v-card-subtitle>
                <v-card-text>
                  <div class="text-h6 mb-2">Estimate: {{ selectedMember.estimate }} days</div>
                  <div class="justification">{{ selectedMember.justification }}</div>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" @click="showModal = false">Close</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>
          <div v-else>
            <p>Loading team estimates...</p>
            <v-progress-circular indeterminate></v-progress-circular>
          </div>
        </v-window-item>
      </v-window>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// Add API base URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

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
  const radius = 200 // Radius of the circle
  const x = Math.cos(angle) * radius
  const y = Math.sin(angle) * radius
  
  return {
    transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`,
    left: '50%',
    top: '50%'
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
  position: 'relative',
  width: '500px',
  height: '500px',
  margin: '3rem auto'
}

const getTeamEstimates = async () => {
  try {
    console.log("Getting team estimates...");
    const response = await fetch(`${API_BASE_URL}/api/estimate/days`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        story: currentAnalysis.value?.original_story
      })
    });
    
    const data = await response.json();
    console.log("Team estimates response:", data);
    
    if (data.team_estimates) {
      teamEstimates.value = data.team_estimates;
    }
  } catch (error) {
    console.error("Error getting team estimates:", error);
  }
};

const showModal = ref(false)
const selectedMember = ref<TeamMember | null>(null)
const averageEstimate = computed(() => {
  if (!teamEstimates.value.length) return 0
  const total = teamEstimates.value.reduce((sum, member) => sum + member.estimate, 0)
  return (total / teamEstimates.value.length).toFixed(1)
})

const showMemberDetails = (member: TeamMember) => {
  selectedMember.value = member
  showModal.value = true
}

const formatAnalysis = (analysis: string | undefined) => {
  if (!analysis) return '';
  // Remove redundant "Analysis:" prefix if it exists
  return analysis.replace(/^Analysis:\s*/, '')
                .replace(/^INVEST Analysis:\s*/, '');
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
  background-color: #1E1E1E;
  padding: 2rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.story-output h3 {
  color: #64B5F6;
  margin-bottom: 1rem;
  font-size: 1.2rem;
  font-weight: 500;
}

.story-output pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  color: rgba(255, 255, 255, 0.87);
  font-family: inherit;
  margin: 0.5rem 0 1.5rem 0;
  line-height: 1.6;
}

.story-output ul {
  list-style-type: none;
  padding-left: 1rem;
  margin: 0.5rem 0 1.5rem 0;
}

.story-output li {
  color: rgba(255, 255, 255, 0.87);
  margin-bottom: 0.5rem;
  position: relative;
  padding-left: 1rem;
}

.story-output li:before {
  content: "•";
  color: #64B5F6;
  position: absolute;
  left: -0.5rem;
}

.analysis {
  margin-top: 2rem;
}

.analysis h3 {
  margin-bottom: 1rem;
}

.suggestions {
  margin-top: 2rem;
}

.suggestions ul {
  padding-left: 0;
}

.suggestions li {
  margin-bottom: 1rem;
}

.suggestions li strong {
  color: #64B5F6;
  margin-right: 0.5rem;
}

.improved-story {
  border-left: 3px solid #64B5F6;
  padding-left: 1.5rem;
  margin: 1.5rem 0;
}

.improved-story pre {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.95);
}

.improved-story ul {
  margin-top: 1rem;
}

.improved-story li {
  color: rgba(255, 255, 255, 0.87);
}

.story-generator-title {
  color: rgba(255, 255, 255, 0.95) !important; /* Almost white */
  margin-bottom: 2rem;
  font-weight: 300; /* Light weight for elegance */
  letter-spacing: 0.5px;
}
</style> 
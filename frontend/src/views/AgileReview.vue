<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column: Primary Content -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <div class="story-section">
            <h3>Improved Story</h3>
            <div class="editable-content">
              <template v-if="!editingStory">
                <pre>{{ storyStore.improvedStory }}</pre>
                <v-btn 
                  size="small" 
                  color="primary" 
                  class="edit-btn"
                  icon="mdi-pencil"
                  @click="startEditingStory"
                ></v-btn>
              </template>
              <template v-else>
                <v-textarea
                  v-model="editedStory"
                  auto-grow
                  variant="outlined"
                  class="edit-textarea"
                ></v-textarea>
                <div class="edit-actions">
                  <v-btn 
                    size="small" 
                    color="success" 
                    @click="saveStory"
                    class="mr-2"
                  >Save</v-btn>
                  <v-btn 
                    size="small" 
                    color="error" 
                    @click="cancelEditStory"
                  >Cancel</v-btn>
                </div>
              </template>
            </div>
            
            <h3>Enhanced Acceptance Criteria</h3>
            <div class="editable-content">
              <template v-if="!editingAC">
                <ul>
                  <li v-for="(criterion, index) in storyStore.acceptanceCriteria" 
                      :key="index">
                    {{ criterion }}
                  </li>
                </ul>
                <v-btn 
                  size="small" 
                  color="primary" 
                  class="edit-btn"
                  icon="mdi-pencil"
                  @click="startEditingAC"
                ></v-btn>
              </template>
              <template v-else>
                <v-textarea
                  v-model="editedAC"
                  auto-grow
                  variant="outlined"
                  placeholder="One acceptance criterion per line"
                  class="edit-textarea"
                ></v-textarea>
                <div class="edit-actions">
                  <v-btn 
                    size="small" 
                    color="success" 
                    @click="saveAC"
                    class="mr-2"
                  >Save</v-btn>
                  <v-btn 
                    size="small" 
                    color="error" 
                    @click="cancelEditAC"
                  >Cancel</v-btn>
                </div>
              </template>
            </div>
          </div>
        </div>
        
        <!-- Sticky footer inside primary-content-wrapper -->
        <div class="sticky-footer">
          <div class="footer-content">
            <v-btn 
              color="primary" 
              size="large"
              prepend-icon="mdi-send"
              :loading="loading"
              :disabled="editingStory || editingAC"
              @click="submitForTechReview"
            >
              Send for Tech Review
            </v-btn>
            <div class="footer-hint" v-if="editingStory || editingAC">
              Save your changes to enable sending for review
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Analysis Panel -->
      <div class="analysis-panel">
        <div class="analysis">
          <h3>Analysis</h3>
          <div class="invest-grid">
            <div v-for="(feedback, index) in storyStore.formatFeedback" 
                 :key="index" 
                 class="invest-item"
                 :class="{ 'warning': feedback.type === 'warning' }">
              <div class="invest-header">
                <span class="invest-letter">{{ feedback.type === 'positive' ? 'P' : 'W' }}</span>
                <span class="invest-title">{{ feedback.type === 'positive' ? 'Positive' : 'Warning' }}</span>
              </div>
              <div class="invest-content">{{ feedback.message }}</div>
            </div>
          </div>
        </div>

        <div class="suggestions mt-6">
          <h3>Clarity Feedback</h3>
          <div class="suggestions-list">
            <div v-for="(feedback, index) in storyStore.clarityFeedback" 
                 :key="index"
                 class="suggestion-item">
              <div class="suggestion-header">{{ feedback.type === 'positive' ? 'Positive' : 'Warning' }}</div>
              <div class="suggestion-content">{{ feedback.message }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStoryStore } from '@/stores/story'

const router = useRouter()
const storyStore = useStoryStore()

// Prevent direct navigation without data
onMounted(() => {
  if (!storyStore.improvedStory) {
    console.warn('No story data found, redirecting to home')
    router.push('/')
    return
  }
})

// Story editing
const editingStory = ref(false)
const editedStory = ref('')

const startEditingStory = () => {
  editedStory.value = storyStore.improvedStory
  editingStory.value = true
}

const saveStory = () => {
  storyStore.improvedStory = editedStory.value
  editingStory.value = false
}

const cancelEditStory = () => {
  editingStory.value = false
}

// AC editing
const editingAC = ref(false)
const editedAC = ref('')

const startEditingAC = () => {
  editedAC.value = storyStore.acceptanceCriteria.join('\n')
  editingAC.value = true
}

const saveAC = () => {
  storyStore.acceptanceCriteria = editedAC.value
    .split('\n')
    .filter(line => line.trim())
  editingAC.value = false
}

const cancelEditAC = () => {
  editingAC.value = false
}

// Submit for tech review
const loading = ref(false)

const submitForTechReview = async () => {
  console.log('Submitting for tech review...')
  loading.value = true
  try {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Navigate to new route
    router.push('/TechReview')
    return true
  } catch (error) {
    console.error('Error submitting for tech review:', error)
    return false
  } finally {
    loading.value = false
  }
}

// Parse INVEST analysis into structured data
const investAnalysis = [
  {
    letter: 'I',
    title: 'Independent',
    content: 'The user story is independent, as it does not seem to depend on any other user story for its implementation.'
  },
  {
    letter: 'N',
    title: 'Negotiable',
    content: 'The story is not very negotiable as it is not clear on what exactly the notification bell should do, or what exactly broadcasting a message entails.'
  },
  {
    letter: 'V',
    title: 'Valuable',
    content: 'The value to the user is not clearly stated. Why should the user care about this new notification bell?'
  },
  {
    letter: 'E',
    title: 'Estimable',
    content: 'The story is too vague to be reliably estimated. We don\'t know what "broadcasting a message" involves.'
  },
  {
    letter: 'S',
    title: 'Small',
    content: 'The story is not small, as it seems to involve several different features or functionalities.'
  },
  {
    letter: 'T',
    title: 'Testable',
    content: 'The acceptance criteria are too vague to be testable. What does it mean for everyone to "get it" and "read it"?'
  }
]

// Add this function to detect negative feedback
const isNegative = (content: string): boolean => {
  const negativeTerms = ['not', 'too vague', 'unclear', 'missing'];
  return negativeTerms.some(term => content.toLowerCase().includes(term));
}
</script>

<style>
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

.primary-content-wrapper {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.primary-content {
  position: sticky;
  top: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
  max-height: calc(100vh - 8rem);
  overflow-y: auto;
  flex-grow: 1;
}

.analysis-panel {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
}

.editable-content {
  position: relative;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
  transition: all 0.3s ease;
}

.edit-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.editable-content:hover .edit-btn {
  opacity: 1;
}

.story-section h3 {
  color: #64B5F6;
  margin-top: 2rem;
}

.story-section h3:first-child {
  margin-top: 0;
}

.editable-content pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  color: rgba(255, 255, 255, 0.87);
  font-family: inherit;
  margin: 0;
  line-height: 1.6;
}

.editable-content ul {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

.editable-content li {
  color: rgba(255, 255, 255, 0.87);
  margin-bottom: 0.5rem;
  padding-left: 1.5rem;
  position: relative;
}

.editable-content li:before {
  content: "•";
  color: #64B5F6;
  position: absolute;
  left: 0;
}

/* Keep existing invest-grid styles */
.invest-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-top: 1rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .two-column-layout {
    grid-template-columns: 1fr;
  }
  
  .primary-content {
    position: relative;
    top: 0;
    max-height: none;
  }
  
  .analysis-panel {
    margin-top: 2rem;
  }
}

/* Updated Analysis Panel Styles */
.analysis-panel {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
}

.analysis-panel h3 {
  color: #64B5F6;
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

/* INVEST Grid Refinements */
.invest-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.invest-item {
  background: rgba(33, 150, 243, 0.1);
  border-radius: 8px;
  padding: 1.25rem;
  border-left: 3px solid #64B5F6;
  transition: transform 0.2s ease;
}

.invest-item.warning {
  border-left-color: #FFA726;
  background: rgba(255, 167, 38, 0.1);
}

.invest-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.invest-letter {
  background: #64B5F6;
  color: #1E1E1E;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 0.75rem;
}

.warning .invest-letter {
  background: #FFA726;
}

/* Suggestions Refinements */
.suggestions-list {
  display: grid;
  gap: 1rem;
}

.suggestion-item {
  background: rgba(33, 150, 243, 0.1);
  border-radius: 8px;
  padding: 1.25rem;
  border-left: 3px solid #64B5F6;
}

.suggestion-header {
  color: #64B5F6;
  font-weight: 500;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.suggestion-content {
  color: rgba(255, 255, 255, 0.87);
  line-height: 1.6;
}

/* Hover effects */
.invest-item:hover, 
.suggestion-item:hover {
  transform: translateY(-2px);
}

/* Responsive adjustments */
@media (max-width: 1400px) {
  .invest-grid {
    grid-template-columns: 1fr;
  }
}

.edit-textarea {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}

/* Style the textarea */
:deep(.v-field__input) {
  color: rgba(255, 255, 255, 0.87) !important;
  font-family: inherit !important;
  line-height: 1.6 !important;
}

:deep(.v-field) {
  border-color: rgba(255, 255, 255, 0.1) !important;
}

.sticky-footer {
  position: fixed;
  bottom: 0;
  width: calc(50% - 2rem);
  background: linear-gradient(
    to top,
    rgba(30, 30, 30, 1) 0%,
    rgba(30, 30, 30, 0.9) 70%,
    rgba(30, 30, 30, 0) 100%
  );
  padding: 1rem 0;
  margin-top: -4rem;
  pointer-events: none;
  z-index: 10;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  pointer-events: auto;
  padding: 0 2rem;
}

.footer-hint {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
}

/* Update responsive styles */
@media (max-width: 1024px) {
  .primary-content {
    position: relative;
    top: 0;
    max-height: none;
  }
  
  .sticky-footer {
    position: fixed;
    width: 100%;
    left: 0;
    right: 0;
    margin-top: 0;
  }
}
</style> 
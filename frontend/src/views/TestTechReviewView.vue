<template>
  <div class="test">
    <div class="two-column-layout">
      <!-- Left Column: Implementation Details -->
      <div class="primary-content-wrapper">
        <div class="primary-content">
          <div class="implementation-section">
            <h3>Implementation Details</h3>
            <div class="tech-section">
              <h4>Frontend</h4>
              <div class="task-list">
                <div v-for="(task, index) in mockTechReviewResult.implementation_details.frontend" 
                     :key="'fe-'+index"
                     class="task-item">
                  <v-icon size="small" color="primary" class="mr-2">mdi-code-tags</v-icon>
                  {{ task }}
                </div>
              </div>

              <h4>Backend</h4>
              <div class="task-list">
                <div v-for="(task, index) in mockTechReviewResult.implementation_details.backend" 
                     :key="'be-'+index"
                     class="task-item">
                  <v-icon size="small" color="primary" class="mr-2">mdi-server</v-icon>
                  {{ task }}
                </div>
              </div>

              <h4>Database</h4>
              <div class="task-list">
                <div v-for="(task, index) in mockTechReviewResult.implementation_details.database" 
                     :key="'db-'+index"
                     class="task-item">
                  <v-icon size="small" color="primary" class="mr-2">mdi-database</v-icon>
                  {{ task }}
                </div>
              </div>
            </div>

            <h3 class="mt-6">Estimated Effort</h3>
            <div class="effort-grid">
              <div v-for="(effort, key) in mockTechReviewResult.estimated_effort" 
                   :key="key"
                   class="effort-item"
                   :class="{ 'effort-total': key === 'total' }">
                <div class="effort-label">{{ key }}</div>
                <div class="effort-value">{{ effort }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sticky footer -->
        <div class="sticky-footer">
          <div class="footer-content">
            <v-btn 
              color="success" 
              prepend-icon="mdi-check-circle"
            >
              Approve Technical Review
            </v-btn>
          </div>
        </div>
      </div>

      <!-- Right Column: Analysis -->
      <div class="analysis-panel">
        <div class="technical-analysis">
          <h3>Technical Analysis</h3>
          <div class="analysis-grid">
            <div v-for="(analysis, key) in mockTechReviewResult.technical_analysis" 
                 :key="key"
                 class="analysis-item">
              <div class="analysis-header">
                <span class="analysis-title">{{ key }}</span>
                <div class="score-badge" :class="getScoreClass(analysis.score)">
                  {{ analysis.score }}/10
                </div>
              </div>
              <div class="analysis-content">{{ analysis.explanation }}</div>
            </div>
          </div>
        </div>

        <div class="risks mt-6">
          <h3>Risks & Considerations</h3>
          <div class="risks-grid">
            <div v-for="(risk, index) in mockTechReviewResult.risks_and_considerations" 
                 :key="index"
                 class="risk-item">
              <div class="risk-header">
                <v-icon color="warning" class="mr-2">mdi-alert</v-icon>
                {{ risk.category }}
              </div>
              <div class="risk-description">{{ risk.description }}</div>
              <div class="risk-mitigation">
                <v-icon color="success" size="small" class="mr-2">mdi-shield</v-icon>
                {{ risk.mitigation }}
              </div>
            </div>
          </div>
        </div>

        <div class="recommendations mt-6">
          <h3>Recommendations</h3>
          <div class="recommendations-list">
            <div v-for="(rec, index) in mockTechReviewResult.recommendations" 
                 :key="index"
                 class="recommendation-item">
              <v-icon color="info" size="small" class="mr-2">mdi-lightbulb</v-icon>
              {{ rec }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { mockTechReviewResult } from '@/mocks/mockTechReviewData'

const getScoreClass = (score: number): string => {
  if (score >= 8) return 'score-high'
  if (score >= 5) return 'score-medium'
  return 'score-low'
}
</script>

<style>
/* Base layout styles (similar to TestFormatView) */
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

/* Implementation Details Styles */
.tech-section {
  margin-top: 1rem;
}

.tech-section h4 {
  color: #64B5F6;
  margin: 1.5rem 0 1rem;
  font-size: 1.1rem;
}

.task-list {
  display: grid;
  gap: 0.75rem;
}

.task-item {
  background: rgba(33, 150, 243, 0.1);
  padding: 0.75rem 1rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
}

/* Effort Grid */
.effort-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.effort-item {
  background: rgba(33, 150, 243, 0.1);
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}

.effort-total {
  background: rgba(33, 150, 243, 0.2);
  font-weight: bold;
}

.effort-label {
  color: #64B5F6;
  font-size: 0.9rem;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.effort-value {
  font-size: 1.2rem;
  font-weight: 500;
}

/* Analysis Panel Styles */
.analysis-panel {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
}

.analysis-grid {
  display: grid;
  gap: 1rem;
  margin-top: 1rem;
}

.analysis-item {
  background: rgba(33, 150, 243, 0.1);
  padding: 1.25rem;
  border-radius: 8px;
}

.analysis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.analysis-title {
  color: #64B5F6;
  font-weight: 500;
  font-size: 1.1rem;
  text-transform: capitalize;
}

.score-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-weight: 500;
  font-size: 0.9rem;
}

.score-high {
  background: rgba(76, 175, 80, 0.2);
  color: #81C784;
}

.score-medium {
  background: rgba(255, 152, 0, 0.2);
  color: #FFB74D;
}

.score-low {
  background: rgba(244, 67, 54, 0.2);
  color: #E57373;
}

/* Risks Styles */
.risks-grid {
  display: grid;
  gap: 1rem;
  margin-top: 1rem;
}

.risk-item {
  background: rgba(33, 150, 243, 0.1);
  padding: 1.25rem;
  border-radius: 8px;
}

.risk-header {
  color: #FFA726;
  font-weight: 500;
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
}

.risk-description {
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.risk-mitigation {
  color: #81C784;
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

/* Recommendations Styles */
.recommendations-list {
  display: grid;
  gap: 0.75rem;
  margin-top: 1rem;
}

.recommendation-item {
  background: rgba(33, 150, 243, 0.1);
  padding: 1rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
}

/* Sticky Footer */
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
  
  .sticky-footer {
    position: fixed;
    width: 100%;
    left: 0;
    right: 0;
    margin-top: 0;
  }
  
  .analysis-panel {
    margin-top: 2rem;
  }
}
</style> 
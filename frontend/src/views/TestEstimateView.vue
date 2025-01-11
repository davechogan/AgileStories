<template>
  <div class="test-estimate">
    <h1>Estimation Layout Test</h1>
    
    <!-- Circle layout with centered average -->
    <div class="estimation-circle" :style="circleStyles">
      <!-- Center average -->
      <div class="average-estimate">
        <div class="average-number">{{ averageEstimate }}</div>
        <div class="average-label">days average</div>
      </div>
      
      <!-- Team members -->
      <div 
        v-for="(member, index) in mockTeamEstimates" 
        :key="member.name"
        class="team-member"
        :style="getPositionStyle(index, mockTeamEstimates.length)"
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
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface TeamMember {
  id: number;
  name: string;
  title: string;
  initials: string;
  color: string;
  estimate: number;
  justification: string;
}

// Mock data
const mockTeamEstimates = ref<TeamMember[]>([
  {
    id: 1,
    name: "Sarah Chen",
    title: "Senior Developer Lead",
    initials: "SC",
    color: "#4ECDC4",
    estimate: 15,
    justification: "As the lead developer, I'm considering the full architectural impact..."
  },
  {
    id: 2,
    name: "Alex Thompson",
    title: "Senior Developer",
    initials: "AT",
    color: "#FF6B6B",
    estimate: 9,
    justification: "Based on similar features we've implemented..."
  },
  {
    id: 3,
    name: "Emily Parker",
    title: "Mid-level Developer",
    initials: "EP",
    color: "#45B7D1",
    estimate: 7,
    justification: "The core functionality seems straightforward..."
  },
  {
    id: 4,
    name: "Michael Rodriguez",
    title: "Senior QA Analyst",
    initials: "MR",
    color: "#96CEB4",
    estimate: 5,
    justification: "Testing scope includes..."
  },
  {
    id: 5,
    name: "Jamie Lee",
    title: "Junior QA Analyst",
    initials: "JL",
    color: "#D4A5A5",
    estimate: 7,
    justification: "Need to consider edge cases..."
  }
])

const showModal = ref(false)
const selectedMember = ref<TeamMember | null>(null)

const averageEstimate = computed(() => {
  if (!mockTeamEstimates.value.length) return 0
  const total = mockTeamEstimates.value.reduce((sum, member) => sum + member.estimate, 0)
  return (total / mockTeamEstimates.value.length).toFixed(1)
})

const getPositionStyle = (index: number, total: number) => {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2
  const radius = 200
  const x = Math.cos(angle) * radius
  const y = Math.sin(angle) * radius
  
  return {
    transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`,
    left: '50%',
    top: '50%'
  }
}

const circleStyles = {
  position: 'relative',
  width: '500px',
  height: '500px',
  margin: '3rem auto'
}

const showMemberDetails = (member: TeamMember) => {
  selectedMember.value = member
  showModal.value = true
}
</script>

<style scoped>
.test-estimate {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.estimation-circle {
  position: relative;
  border: 2px dashed #eee;
  border-radius: 50%;
}

.average-estimate {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  background: rgba(33, 150, 243, 0.1);
  padding: 1rem;
  border-radius: 50%;
  width: 120px;
  height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.average-number {
  font-size: 2rem;
  font-weight: bold;
  color: #2196F3;
}

.average-label {
  font-size: 0.8rem;
  color: #666;
}

.team-member {
  position: absolute;
  text-align: center;
  transition: all 0.3s ease;
  width: 120px;
}

.member-avatar {
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.member-avatar:hover {
  transform: scale(1.1);
}

.member-info {
  font-size: 0.8rem;
  white-space: nowrap;
}

.member-name {
  font-weight: bold;
}

.member-title {
  color: #666;
  font-size: 0.7rem;
}

.member-estimate {
  color: #2196F3;
  font-weight: bold;
  margin-top: 0.2rem;
}
</style> 
<template>
  <div class="test-estimate">
    <div class="header-container">
      <h1 class="text-h4 page-title">Estimation Layout Test</h1>
    </div>
    
    <!-- Avatar style controls -->
    <div class="avatar-controls">
      <v-btn-group vertical density="compact">
        <v-btn color="primary" size="small" @click="regenerateAvatars">Regenerate All</v-btn>
        <v-btn color="primary" size="small" @click="cycleAvatarStyle">Change Style</v-btn>
      </v-btn-group>
      <div class="current-style text-secondary">Current Style: {{ currentAvatarStyle }}</div>
    </div>
    
    <!-- Circle layout with centered average -->
    <div class="estimation-circle" :style="circleStyles">
      <div class="average-estimate">
        <div class="average-number">{{ averageEstimate }}</div>
        <div class="average-label">days average</div>
      </div>
      
      <div 
        v-for="(member, index) in mockTeamEstimates" 
        :key="member.id"
        class="team-member"
        :style="getPositionStyle(index, mockTeamEstimates.length)"
      >
        <v-avatar
          size="60"
          class="member-avatar"
          @click="showMemberDetails(member)"
        >
          <v-img :src="member.avatarUrl"></v-img>
        </v-avatar>
        <div class="member-info">
          <div class="member-name">{{ member.name }}</div>
          <div class="member-title">{{ member.title }}</div>
          <div class="member-estimate">{{ member.estimate }} days</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// Avatar styles available in DiceBear
const avatarStyles = [
  'adventurer',
  'adventurer-neutral',
  'avataaars',
  'avataaars-neutral',
  'big-ears',
  'big-ears-neutral',
  'big-smile',
  'bottts',
  'bottts-neutral',
  'croodles',
  'croodles-neutral',
  'fun-emoji',
  'icons',
  'identicon',
  'initials',
  'lorelei',
  'lorelei-neutral',
  'micah',
  'miniavs',
  'notionists',
  'notionists-neutral',
  'open-peeps',
  'personas',
  'pixel-art',
  'pixel-art-neutral',
  'shapes',
  'thumbs'
]

const currentAvatarStyle = ref('adventurer')
const currentStyleIndex = ref(0)

// Mock team data
interface TeamMember {
  id: number
  name: string
  title: string
  estimate: number
  avatarUrl: string
}

const mockTeamEstimates = ref<TeamMember[]>([
  {
    id: 1,
    name: 'Sarah Chen',
    title: 'Senior Developer Lead',
    estimate: 15,
    avatarUrl: ''
  },
  {
    id: 2,
    name: 'Jamie Lee',
    title: 'Junior QA Analyst',
    estimate: 7,
    avatarUrl: ''
  },
  {
    id: 3,
    name: 'Alex Thompson',
    title: 'Senior Developer',
    estimate: 9,
    avatarUrl: ''
  },
  {
    id: 4,
    name: 'Michael Rodriguez',
    title: 'Senior QA Analyst',
    estimate: 5,
    avatarUrl: ''
  },
  {
    id: 5,
    name: 'Emily Parker',
    title: 'Mid-level Developer',
    estimate: 7,
    avatarUrl: ''
  }
])

// Initial random positions for animation
const initialPositions = ref(new Map())

const getRandomPosition = () => {
  const randomX = (Math.random() - 0.5) * window.innerWidth
  const randomY = (Math.random() - 0.5) * window.innerHeight
  return { x: randomX, y: randomY }
}

// Initialize random positions when team changes
const initializePositions = () => {
  mockTeamEstimates.value.forEach(member => {
    initialPositions.value.set(member.id, getRandomPosition())
  })
  // Trigger reflow to ensure animation works
  setTimeout(() => {
    initialPositions.value = new Map()
  }, 50)
}

// Calculate average estimate
const averageEstimate = computed(() => {
  const total = mockTeamEstimates.value.reduce((sum, member) => sum + member.estimate, 0)
  return (total / mockTeamEstimates.value.length).toFixed(1)
})

// Calculate circle size based on viewport
const circleStyles = computed(() => {
  const size = Math.min(window.innerWidth * 0.8, 800)
  return {
    width: `${size}px`,
    height: `${size}px`
  }
})

// Calculate position for each team member
const getPositionStyle = (index: number, total: number) => {
  const angle = (index * 360) / total - 90 // Start from top
  const radius = 200 // Fixed radius in pixels instead of percentage
  
  // Get initial random position if it exists
  const initialPos = initialPositions.value.get(mockTeamEstimates.value[index].id)
  
  if (initialPos) {
    return {
      position: 'absolute',
      left: `${initialPos.x}px`,
      top: `${initialPos.y}px`,
      transform: 'translate(-50%, -50%)',
      transition: 'none'
    }
  }
  
  const angleInRad = (angle * Math.PI) / 180
  const x = Math.cos(angleInRad) * radius
  const y = Math.sin(angleInRad) * radius
  
  return {
    position: 'absolute',
    left: '50%',
    top: '50%',
    transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`,
    transition: 'all 1s cubic-bezier(0.34, 1.56, 0.64, 1)'
  }
}

// Generate new avatar URLs
const regenerateAvatars = () => {
  mockTeamEstimates.value.forEach(member => {
    const seed = Math.random().toString(36).substring(7)
    member.avatarUrl = `https://api.dicebear.com/7.x/${currentAvatarStyle.value}/svg?seed=${seed}`
  })
  initializePositions()
}

// Cycle through avatar styles
const cycleAvatarStyle = () => {
  currentStyleIndex.value = (currentStyleIndex.value + 1) % avatarStyles.length
  currentAvatarStyle.value = avatarStyles[currentStyleIndex.value]
  regenerateAvatars()
}

// Show member details (placeholder)
const showMemberDetails = (member: TeamMember) => {
  console.log('Show details for:', member.name)
}

// Initialize avatars on mount
onMounted(() => {
  regenerateAvatars()
})
</script>

<style>
.test-estimate {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  display: flex;
  flex-direction: column;
}

.header-container {
  position: absolute;
  left: 2rem;
  top: 1rem;
  width: 200px;
}

.page-title {
  text-align: left;
  font-size: 1.5rem !important;
  line-height: 1.2 !important;
  margin: 0 !important;
}

.avatar-controls {
  position: fixed;
  bottom: 1.5rem;
  left: 1.5rem;
  z-index: 1000;
  scale: 0.9;
}

.current-style {
  margin-top: 0.3rem;
  font-size: 0.75rem;
  opacity: 0.7;
}

.estimation-circle {
  position: relative;
  margin: -2rem auto 0;
  padding-top: 2rem;
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
  opacity: 0.7;
}

.team-member {
  position: absolute;
  text-align: center;
  transition: all 1s cubic-bezier(0.34, 1.56, 0.64, 1);
  width: 120px;
}

.member-avatar {
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: transform 0.2s;
  background: white;
  opacity: 0;
  animation: fadeIn 0.5s forwards;
  animation-delay: 0.5s;
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
  opacity: 0.7;
  font-size: 0.7rem;
  margin: 0.2rem 0;
}

.member-estimate {
  color: #2196F3;
  font-weight: bold;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 768px) {
  .avatar-controls {
    bottom: 1rem;
    left: 1rem;
  }
  
  .current-style {
    font-size: 0.7rem;
  }
}
</style> 
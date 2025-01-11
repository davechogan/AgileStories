<template>
  <v-app>
    <DevNav />
    
    <!-- Global loading overlay -->
    <v-overlay
      :model-value="loading"
      class="align-center justify-center"
      persistent
    >
      <v-progress-circular
        color="primary"
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>
    
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DevNav from '@/components/DevNav.vue'

const route = useRoute()
const loading = ref(false)

// Show loading during route changes
watch(
  () => route.path,
  async () => {
    loading.value = true
    await new Promise(resolve => setTimeout(resolve, 500))
    loading.value = false
  }
)
</script>

<style>
.v-main {
  background: #121212;
}
</style> 
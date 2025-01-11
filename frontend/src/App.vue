<template>
  <v-app :theme="theme" :class="theme">
    <v-app-bar :class="`${theme}-theme`" flat>
      <v-app-bar-title class="app-title">Story Generator</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn to="/">HOME</v-btn>
      <v-btn to="/test-story-analysis">TEST STORY ANALYSIS</v-btn>
      <v-btn icon @click="toggleTheme" class="ml-4">
        <v-icon>{{ theme === 'dark' ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main :class="`${theme}-theme`">
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import RouterDebug from './components/RouterDebug.vue'
</script>

<style>
/* Global styles if needed */

.app-title {
  color: rgba(255, 255, 255, 0.95) !important; /* Much lighter, almost white */
  font-weight: 300; /* Lighter font weight */
  letter-spacing: 0.5px; /* Slight letter spacing for better readability */
}
</style> 
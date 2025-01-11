<template>
  <v-app>
    <v-main>
      <!-- Navigation -->
      <v-app-bar>
        <v-container class="d-flex align-center">
          <v-app-bar-title>Agile Stories</v-app-bar-title>
          <v-spacer />
          <v-btn to="/" text>Home</v-btn>
          <v-btn to="/test" text>Test Story Analysis</v-btn>
        </v-container>
      </v-app-bar>

      <!-- Main content -->
      <v-container>
        <router-view />
        <RouterDebug v-if="false" />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import RouterDebug from './components/RouterDebug.vue'
</script>

<style>
/* Global styles if needed */
</style> 
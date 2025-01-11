import { defineStore } from 'pinia'

export const useStoryStore = defineStore('story', {
  state: () => ({
    currentAnalysis: null
  }),
  
  actions: {
    setCurrentAnalysis(analysis) {
      this.currentAnalysis = analysis
    }
  }
}) 
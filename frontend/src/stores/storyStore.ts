import { defineStore } from 'pinia'
import type { AnalysisResult } from '@/types'

export const useStoryStore = defineStore('story', {
  state: () => ({
    currentAnalysis: null as AnalysisResult | null
  }),
  
  actions: {
    setAnalysis(analysis: AnalysisResult) {
      this.currentAnalysis = analysis
    },
    
    clearAnalysis() {
      this.currentAnalysis = null
    }
  }
}) 
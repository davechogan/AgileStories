export interface Story {
  text: string
  acceptance_criteria: string[]
  context: string
  version?: number
}

// Raw response from API
export interface AnalysisResult {
  original_story: Story
  improved_story: {
    text: string
    acceptance_criteria: string[]
  } | null
  analysis: string
  suggestions: Record<string, string>
  status: string
  timestamp: string
}

// Formatted for UI (matches TestFormatView)
export interface MockAnalysisResult {
  improved_story: {
    text: string
    acceptance_criteria: string[]
  }
  suggestions: Record<string, string>
  invest_analysis: Array<{
    letter: string
    title: string
    content: string
  }>
} 
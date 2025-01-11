export interface Story {
  text: string
  acceptance_criteria: string[]
  context: string
  version: number
}

export interface AnalysisResult {
  improved_story: {
    text: string
    acceptance_criteria: string[]
  }
  analysis: string
  suggestions?: Record<string, string>
}

export interface MockAnalysisResult {
  improved_story: {
    text: string
    acceptance_criteria: string[]
  }
  invest_analysis: Array<{
    letter: string
    title: string
    content: string
  }>
  suggestions: Record<string, string>
} 
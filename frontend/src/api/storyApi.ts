import axios from 'axios'
import type { Story, AnalysisResult, MockAnalysisResult } from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Constants from TestFormatView
const INVEST_ORDER = [
  'Independent',
  'Negotiable',
  'Valuable',
  'Estimable',
  'Small',
  'Testable'
] as const

const LETTER_COLORS = {
  'I': '#FFA726',
  'N': '#FFA726',
  'V': '#FFA726',
  'E': '#FFA726',
  'S': '#FFA726',
  'T': '#FFA726'
} as const

const SECTION_TITLES = {
  story: 'Improved Story',
  criteria: 'Enhanced Acceptance Criteria',
  analysis: 'Analysis'
} as const

const transformAnalysis = (rawAnalysis: AnalysisResult): MockAnalysisResult => {
  // Transform INVEST analysis in correct order
  const investAnalysis = INVEST_ORDER.map(criterion => {
    const letter = criterion[0]
    const analysisText = rawAnalysis.analysis
      .split('\n')
      .filter(line => line.includes(criterion + ':'))
      .map(line => line
        .replace(`${criterion}:`, '')
        .trim()
      )
      .join(' ')

    return {
      letter,
      title: criterion,
      content: analysisText
    }
  })

  // Extract suggestions with new format
  const additionalSuggestions = rawAnalysis.analysis
    .split('Additional Suggestions:')
    .pop()
    ?.trim()

  const suggestions: Record<string, string> = additionalSuggestions 
    ? {
        'Improvements': additionalSuggestions
      }
    : rawAnalysis.suggestions || {}

  return {
    improved_story: {
      text: rawAnalysis.improved_story?.text || '',
      acceptance_criteria: rawAnalysis.improved_story?.acceptance_criteria || []
    },
    invest_analysis: investAnalysis,
    suggestions
  }
}

// Add the API function back with original endpoint
export async function submitStoryForAgileReview(story: Story): Promise<MockAnalysisResult> {
  try {
    const response = await api.post<AnalysisResult>('/api/analyze', story)
    return transformAnalysis(response.data)
  } catch (error) {
    console.error('Error submitting story:', error)
    throw error
  }
}

export {
  transformAnalysis,
  INVEST_ORDER,
  LETTER_COLORS,
  SECTION_TITLES,
  type MockAnalysisResult
} 
import { transformAnalysis } from '@/api/storyApi'

describe('Story API Transformation', () => {
  it('transforms API response to match UI format', () => {
    // Sample API response
    const apiResponse = {
      original_story: {
        text: "As a user, I want to reset my password",
        acceptance_criteria: ["Must be secure"],
        context: "Security feature"
      },
      improved_story: {
        text: "As a user, I want to securely reset my password",
        acceptance_criteria: ["Must meet security requirements"]
      },
      analysis: "INVEST Analysis:\n- Independent: Score: 4 Good independence...",
      suggestions: {
        "clarity": "Add more context"
      },
      status: "complete",
      timestamp: "2024-01-01"
    }

    // Transform
    const result = transformAnalysis(apiResponse)

    // Verify structure matches TestFormatView expectations
    expect(result).toHaveProperty('improved_story')
    expect(result).toHaveProperty('suggestions')
    expect(result).toHaveProperty('invest_analysis')
    
    // Verify INVEST analysis format
    expect(result.invest_analysis[0]).toEqual({
      letter: 'I',
      title: 'Independent',
      content: expect.stringContaining('Score: 4')
    })
  })
}) 
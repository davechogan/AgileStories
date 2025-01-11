import gql from 'graphql-tag'
import type { AnalyzeStoryResponse, AnalyzeStoryVariables } from '@/types/story'

export const ANALYZE_STORY = gql`
  mutation AnalyzeStory($input: StoryInput!) {
    analyzeStory(input: $input) {
      id
      story
      acceptanceCriteria
      analysis {
        agileCoach {
          analysis
          recommendations
          risks
        }
        seniorDev {
          analysis
          technicalDetails {
            feasibility
            complexity
            dependencies
            risks
          }
          risks
        }
        teamEstimates {
          days {
            average
            individual {
              name
              role
              estimate
              confidence
            }
          }
          points {
            average
            fibonacci
            individual {
              name
              role
              estimate
              confidence
            }
          }
        }
      }
    }
  }
`

// Type-safe mutation hook
export function useAnalyzeStory() {
  return useMutation<AnalyzeStoryResponse, AnalyzeStoryVariables>(ANALYZE_STORY)
} 
// Base types
export interface TeamMember {
  name: string;
  role: string;
  experience: number;
}

export interface Estimate {
  name: string;
  role: string;
  estimate: number;
  confidence: 'High' | 'Medium' | 'Low';
}

// Analysis types
export interface AgileCoachAnalysis {
  analysis: string;
  recommendations: string[];
  risks: string[];
}

export interface SeniorDevAnalysis {
  analysis: string;
  technicalDetails: {
    feasibility: string;
    complexity: string;
    dependencies: string[];
    risks: string[];
  };
  risks: string[];
}

export interface TeamEstimates {
  days: {
    average: number;
    individual: Estimate[];
  };
  points: {
    average: number;
    fibonacci: number;
    individual: Estimate[];
  };
}

// Story types
export interface StoryInput {
  story: string;
  acceptanceCriteria: string[];
  context?: string;
}

export interface StoryAnalysis {
  id: string;
  story: string;
  acceptanceCriteria: string[];
  analysis: {
    agileCoach: AgileCoachAnalysis;
    seniorDev: SeniorDevAnalysis;
    teamEstimates: TeamEstimates;
  };
}

// GraphQL response types
export interface AnalyzeStoryResponse {
  analyzeStory: StoryAnalysis;
}

export interface AnalyzeStoryVariables {
  input: StoryInput;
} 
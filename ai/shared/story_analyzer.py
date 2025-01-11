import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Story:
    text: str
    acceptance_criteria: List[str]
    context: str
    version: int = 1
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class AnalysisResult:
    original_story: Story
    analysis: str
    suggestions: Dict[str, Any]
    status: str
    timestamp: str = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'original_story': self.original_story.to_dict(),
            'analysis': self.analysis,
            'suggestions': self.suggestions,
            'status': self.status,
            'timestamp': self.timestamp
        }

class StoryAnalyzer:
    """Handles parallel analysis of user stories"""
    
    def __init__(self):
        self.openai = openai
        self.openai.api_key = os.getenv('OPENAI_API_KEY')
        self.openai.organization = os.getenv('OPENAI_ORG_ID')
        
    def analyze_story(self, story: Story) -> Dict[str, AnalysisResult]:
        """
        Perform parallel analysis of the story from both Agile and Technical perspectives
        """
        # Run both analyses in parallel (in future we could use asyncio)
        agile_result = self._agile_analysis(story)
        tech_result = self._technical_analysis(story)
        
        return {
            'agile': agile_result,
            'technical': tech_result,
            'timestamp': datetime.now().isoformat()
        }
    
    def _agile_analysis(self, story: Story) -> AnalysisResult:
        """Analyze story from Agile perspective"""
        prompt = self._create_agile_prompt(story)
        
        try:
            response = self.openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an experienced Agile Coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            analysis = response.choices[0].message.content
            
            # Parse the analysis into structured suggestions
            suggestions = {
                'improved_story': self._extract_improved_story(analysis),
                'acceptance_criteria': self._extract_acceptance_criteria(analysis),
                'invest_analysis': self._extract_invest_analysis(analysis)
            }
            
            return AnalysisResult(
                original_story=story,
                analysis=analysis,
                suggestions=suggestions,
                status='success'
            )
            
        except Exception as e:
            print(f"Agile analysis error: {str(e)}")
            return AnalysisResult(
                original_story=story,
                analysis=str(e),
                suggestions={},
                status='error'
            )
    
    def _technical_analysis(self, story: Story) -> AnalysisResult:
        """Analyze story from Technical perspective"""
        prompt = self._create_technical_prompt(story)
        
        try:
            response = self.openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an experienced Senior Developer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            analysis = response.choices[0].message.content
            
            # Parse the analysis into structured suggestions
            suggestions = {
                'technical_feasibility': self._extract_feasibility(analysis),
                'implementation_details': self._extract_implementation_details(analysis),
                'complexity': self._extract_complexity(analysis)
            }
            
            return AnalysisResult(
                original_story=story,
                analysis=analysis,
                suggestions=suggestions,
                status='success'
            )
            
        except Exception as e:
            print(f"Technical analysis error: {str(e)}")
            return AnalysisResult(
                original_story=story,
                analysis=str(e),
                suggestions={},
                status='error'
            )
    
    def _create_agile_prompt(self, story: Story) -> str:
        return f"""Analyze this user story using INVEST criteria:

Story: {story.text}

Acceptance Criteria:
{self._format_list(story.acceptance_criteria)}

Context: {story.context}

Please provide:
1. INVEST Analysis
2. Improved version of the story
3. Enhanced acceptance criteria
4. Areas for clarification

Focus on making the story Independent, Negotiable, Valuable, Estimable, Small, and Testable."""

    def _create_technical_prompt(self, story: Story) -> str:
        return f"""Review this user story for technical implementation:

Story: {story.text}

Acceptance Criteria:
{self._format_list(story.acceptance_criteria)}

Context: {story.context}

Please provide:
1. Technical feasibility analysis
2. Implementation approach
3. Potential challenges
4. Required dependencies
5. Complexity estimate (Low/Medium/High)"""

    @staticmethod
    def _format_list(items: List[str]) -> str:
        return "\n".join(f"- {item}" for item in items) if items else "None provided"
    
    # Helper methods to extract structured data from analysis text
    def _extract_improved_story(self, analysis: str) -> str:
        # TODO: Implement extraction logic
        return "Extraction not implemented"
    
    def _extract_acceptance_criteria(self, analysis: str) -> List[str]:
        # TODO: Implement extraction logic
        return []
    
    def _extract_invest_analysis(self, analysis: str) -> Dict[str, str]:
        # TODO: Implement extraction logic
        return {}
    
    def _extract_feasibility(self, analysis: str) -> str:
        # TODO: Implement extraction logic
        return "Extraction not implemented"
    
    def _extract_implementation_details(self, analysis: str) -> Dict[str, Any]:
        # TODO: Implement extraction logic
        return {}
    
    def _extract_complexity(self, analysis: str) -> str:
        # TODO: Implement extraction logic
        return "Medium" 
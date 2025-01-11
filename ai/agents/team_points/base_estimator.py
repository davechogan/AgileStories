from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import openai

class BaseTeamMemberPoints(ABC):
    """Base class for all team members using story points"""
    
    def __init__(self, name: str, role: str, experience_years: int):
        self.name = name
        self.role = role
        self.experience_years = experience_years
        self.fibonacci_points = [1, 2, 3, 5, 8, 13, 21]  # Standard Fibonacci sequence for points
    
    @abstractmethod
    def get_prompt(self, story: str, acceptance_criteria: list, context: str) -> str:
        """Return the specific prompt for this team member"""
        pass
    
    def estimate_effort(self, event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        """
        Estimate effort for the story based on team member's experience
        Returns estimate in story points following Fibonacci sequence
        """
        try:
            # Get the story details from the event body
            if isinstance(event.get('body'), str):
                body = json.loads(event.get('body', '{}'))
            else:
                body = event.get('body', {})
                
            story_text = body.get('story', '')
            acceptance_criteria = body.get('acceptance_criteria', [])
            context = body.get('context', '')
            
            # Get the specific prompt for this team member
            prompt = self.get_prompt(story_text, acceptance_criteria, context)
            
            # Make OpenAI call
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"""You are a {self.role} with {self.experience_years} years of experience.
                    When estimating, you MUST use the Fibonacci sequence: {self.fibonacci_points} points.
                    Choose the number that best represents the complexity and effort required."""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            analysis = response.choices[0].message.content
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'team_member': {
                        'name': self.name,
                        'role': self.role,
                        'experience': self.experience_years
                    },
                    'analysis': analysis,
                    'status': 'success'
                })
            }
            
        except Exception as e:
            print(f"Error in estimate_effort: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': str(e),
                    'status': 'error'
                })
            } 
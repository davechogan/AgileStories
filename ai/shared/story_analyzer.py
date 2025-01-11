import os
import json
import sys
import boto3
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import traceback

# Debug logging
print("StoryAnalyzer: Python path:", sys.path)
print("StoryAnalyzer: Current directory:", os.getcwd())
try:
    import openai
    print("StoryAnalyzer: OpenAI package found:", openai.__file__)
except Exception as e:
    print("StoryAnalyzer: Error importing openai:", str(e))

@dataclass
class Story:
    text: str
    acceptance_criteria: List[str]
    context: str = ""
    version: int = 1
    
    def to_dict(self) -> Dict:
        return asdict(self)

class AnalysisStatus(Enum):
    PENDING = "pending"
    AGILE_REVIEW = "agile_review"
    USER_REVIEW_AGILE = "user_review_agile"
    TECHNICAL_REVIEW = "technical_review"
    USER_REVIEW_FINAL = "user_review_final"
    COMPLETE = "complete"
    ERROR = "error"

@dataclass
class AnalysisResult:
    original_story: Story
    improved_story: Optional[Story]
    analysis: str
    suggestions: Dict[str, Any]
    status: AnalysisStatus
    timestamp: str = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'original_story': self.original_story.to_dict(),
            'improved_story': self.improved_story.to_dict() if self.improved_story else None,
            'analysis': self.analysis,
            'suggestions': self.suggestions,
            'status': self.status.value,
            'timestamp': self.timestamp
        }

class StoryAnalyzer:
    """Handles sequential story analysis workflow"""
    
    def __init__(self):
        """Initialize the StoryAnalyzer"""
        # Import OpenAI here to ensure environment is loaded
        import openai
        
        # Configure OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        openai.organization = os.getenv('OPENAI_ORG_ID')
        
        # No need for Lambda client if we're calling functions directly
        self.agile_coach = __import__('ai.agents.agile_coach.lambda_handler', fromlist=['lambda_handler']).lambda_handler
        self.senior_dev = __import__('ai.agents.senior_dev.lambda_handler', fromlist=['lambda_handler']).lambda_handler
    
    def start_analysis(self, story: Story) -> AnalysisResult:
        """
        Start the analysis workflow with Agile Coach review
        """
        try:
            print(f"StoryAnalyzer.start_analysis: Starting with story: {story}")
            # Add more detailed logging here
            try:
                import openai
                print("OpenAI import successful in start_analysis")
            except Exception as e:
                print(f"OpenAI import failed in start_analysis: {str(e)}")
                print(f"Current sys.path: {sys.path}")
            
            print(f"Starting analysis for story: {story.text}")
            
            # Create the event structure for Lambda
            event = {
                'body': {
                    'story': story.text,
                    'acceptance_criteria': story.acceptance_criteria,
                    'context': story.context
                }
            }
            
            # Call the Agile Coach Lambda handler
            from ai.agents.agile_coach.lambda_handler import lambda_handler
            response = lambda_handler(event, None)
            
            return self._parse_lambda_response(response, story, AnalysisStatus.AGILE_REVIEW)
            
        except Exception as e:
            print(f"Error in start_analysis: {str(e)}")
            return AnalysisResult(
                original_story=story,
                improved_story=None,
                analysis=str(e),
                suggestions={},
                status=AnalysisStatus.ERROR
            )
    
    def _get_value(self, obj, key, default=None):
        """Get value from either object attribute or dictionary key"""
        if hasattr(obj, key):
            return getattr(obj, key)
        elif isinstance(obj, dict):
            return obj.get(key, default)
        return default
    
    def process_user_feedback(self, analysis_result, approved: bool) -> Dict[str, Any]:
        """Process user feedback on analysis"""
        try:
            print("\n=== Processing User Feedback ===")
            print("Analysis Result:")
            print("- Status:", self._get_value(analysis_result, 'status'))
            print("- Has improved story:", bool(self._get_value(analysis_result, 'improved_story')))
            
            if approved:
                # Extract story from the analysis result
                story_data = None
                improved_story = self._get_value(analysis_result, 'improved_story')
                if improved_story:
                    story_data = improved_story if isinstance(improved_story, Story) else Story(**improved_story)
                else:
                    original_story = self._get_value(analysis_result, 'original_story')
                    story_data = original_story if isinstance(original_story, Story) else Story(**original_story)
                
                # Create event for Lambda
                event = {
                    'body': {
                        'story': story_data.text,
                        'acceptance_criteria': story_data.acceptance_criteria,
                        'context': story_data.context
                    }
                }
                
                try:
                    # Call Senior Dev function directly
                    print("Calling Senior Dev function...")
                    result = self.senior_dev(event, None)
                    print("Raw Senior Dev result:", result)
                    print("Result type:", type(result))
                    
                    if isinstance(result, str):
                        result = json.loads(result)
                    if isinstance(result.get('body'), str):
                        result['body'] = json.loads(result['body'])
                    
                    print("Processed Senior Dev result:", json.dumps(result, indent=2))
                    
                    return {
                        'original_story': story_data.to_dict(),
                        'improved_story': story_data.to_dict() if improved_story else None,
                        'analysis': result.get('body', {}).get('analysis', ''),
                        'suggestions': result.get('body', {}).get('suggestions', {}),
                        'status': 'technical_review',
                        'timestamp': datetime.now().isoformat()
                    }
                    
                except Exception as e:
                    print("\nError in Senior Dev call:")
                    print("Exception:", str(e))
                    print("Event data:", json.dumps(event, indent=2))
                    import traceback
                    print("Full traceback:", traceback.format_exc())
                    raise
                    
            else:
                return {
                    'status': 'input',
                    'message': 'Story rejected, returning to input',
                    'original_story': self._get_value(analysis_result, 'original_story'),
                    'improved_story': None,
                    'analysis': '',
                    'suggestions': {},
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            print("\nError in process_user_feedback:")
            print("Exception:", str(e))
            print("Raw analysis_result:", json.dumps(analysis_result, indent=2))
            import traceback
            print("Full traceback:", traceback.format_exc())
            return {
                'status': 'error',
                'message': str(e),
                'original_story': self._get_value(analysis_result, 'original_story'),
                'improved_story': None,
                'analysis': '',
                'suggestions': {},
                'timestamp': datetime.now().isoformat()
            }
    
    def technical_review(self, story: Story) -> AnalysisResult:
        """
        Perform technical review with Senior Dev
        """
        try:
            print(f"\nStarting technical review with story: {story.text}")
            
            # Create the event structure
            event = {
                'body': {
                    'story': story.text,
                    'acceptance_criteria': story.acceptance_criteria,
                    'context': story.context
                }
            }
            
            # Import and call the Lambda handler directly
            from ai.agents.senior_dev.lambda_handler import lambda_handler
            tech_response = lambda_handler(event, None)
            
            return self._parse_lambda_response(tech_response, story, AnalysisStatus.TECHNICAL_REVIEW)
            
        except Exception as e:
            print(f"Error in technical_review: {str(e)}")
            return AnalysisResult(
                original_story=story,
                improved_story=None,
                analysis=str(e),
                suggestions={},
                status=AnalysisStatus.ERROR
            )
    
    def _invoke_lambda(self, function_name: str, event: Dict) -> Dict:
        """
        Invoke a Lambda function and return its response
        """
        try:
            print(f"Invoking {function_name} with event: {json.dumps(event, indent=2)}")
            
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(event)
            )
            
            return json.loads(response['Payload'].read().decode())
            
        except Exception as e:
            print(f"Error invoking {function_name}: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': str(e),
                    'status': 'error'
                })
            }
    
    def _parse_lambda_response(self, lambda_response: Dict, original_story: Story, status: AnalysisStatus) -> AnalysisResult:
        """
        Parse the Lambda response into an AnalysisResult
        """
        try:
            # Handle the response body whether it's a string or dict
            if isinstance(lambda_response.get('body'), str):
                body = json.loads(lambda_response.get('body', '{}'))
            else:
                body = lambda_response.get('body', {})
            
            print(f"Parsed Lambda response body: {json.dumps(body, indent=2)}")
            
            # Extract improved story from the analysis
            improved_story = self._extract_improved_story(body.get('analysis', ''), original_story)
            print(f"Extracted improved story: {improved_story.text if improved_story else 'None'}")  # Debug log
            
            return AnalysisResult(
                original_story=original_story,
                improved_story=improved_story,
                analysis=body.get('analysis', ''),
                suggestions=body.get('suggestions', {}),
                status=status
            )
            
        except Exception as e:
            print(f"Error parsing Lambda response: {str(e)}")
            return AnalysisResult(
                original_story=original_story,
                improved_story=None,
                analysis=str(e),
                suggestions={},
                status=AnalysisStatus.ERROR
            )
    
    def _extract_improved_story(self, analysis: str, original_story: Story) -> Optional[Story]:
        """Extract improved story from analysis text."""
        try:
            print("\n=== Extracting Improved Story ===")
            print("Full analysis text:")
            print(analysis)
            
            # Look for improved story section with flexible matching
            possible_markers = [
                "\nImproved Story:\n",
                "Improved Story:",
                "\nImproved User Story:\n",
                "\nEnhanced Story:\n",
                "\nIMPROVED STORY:\n"
            ]
            
            # Find the story section
            story_start = -1
            for marker in possible_markers:
                story_start = analysis.find(marker)
                if story_start != -1:
                    print(f"Found marker: '{marker}' at position {story_start}")
                    story_start += len(marker)
                    break
            
            if story_start == -1:
                print("No story marker found in text:")
                print("---")
                print(analysis)
                print("---")
                return None
                
            # Find acceptance criteria section
            possible_ac_markers = [
                "\nEnhanced Acceptance Criteria:\n",
                "\nAcceptance Criteria:\n",
                "Enhanced Acceptance Criteria:",
                "Acceptance Criteria:",
                "\nACCEPTANCE CRITERIA:\n"
            ]
            
            story_end = -1
            for marker in possible_ac_markers:
                story_end = analysis.find(marker, story_start)
                if story_end != -1:
                    print(f"Found AC marker: '{marker}' at position {story_end}")
                    break
            
            if story_end == -1:
                story_end = len(analysis)
                
            # Extract and clean the story text
            story_text = analysis[story_start:story_end].strip()
            print(f"\nExtracted story text: '{story_text}'")
            
            # Extract acceptance criteria
            ac_start = -1
            for marker in possible_ac_markers:
                ac_start = analysis.find(marker)
                if ac_start != -1:
                    print(f"Found AC marker for extraction: '{marker}'")
                    ac_start += len(marker)
                    break
            
            acceptance_criteria = []
            if ac_start != -1:
                ac_end = analysis.find("\nAdditional Suggestions:", ac_start)
                if ac_end == -1:
                    ac_end = len(analysis)
                
                ac_text = analysis[ac_start:ac_end].strip()
                print(f"\nRaw AC text:\n{ac_text}")
                
                acceptance_criteria = [
                    criterion.strip('- ').strip()
                    for criterion in ac_text.split('\n')
                    if criterion.strip('- ').strip()
                ]
                print(f"\nExtracted acceptance criteria: {acceptance_criteria}")
            
            if story_text and acceptance_criteria:
                improved_story = Story(
                    text=story_text,
                    acceptance_criteria=acceptance_criteria,
                    context=original_story.context,
                    version=original_story.version + 1
                )
                print(f"\nCreated improved story: {improved_story}")
                return improved_story
                
            print("\nMissing story text or acceptance criteria")
            return None
            
        except Exception as e:
            print(f"Error extracting improved story: {str(e)}")
            print(f"Full traceback: {traceback.format_exc()}")
            return None 
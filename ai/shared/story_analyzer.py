import os
import json
import boto3
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

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
        """Initialize with SAM local endpoint"""
        self.lambda_client = boto3.client(
            'lambda',
            endpoint_url='http://localhost:3001',  # SAM local endpoint
            region_name='us-east-1',
            aws_access_key_id='dummy',
            aws_secret_access_key='dummy',
            verify=False
        )
    
    def start_analysis(self, story: Story) -> AnalysisResult:
        """
        Start the analysis workflow with Agile Coach review
        """
        try:
            # Prepare the event payload
            event = {
                'body': {
                    'story': story.text,
                    'acceptance_criteria': story.acceptance_criteria,
                    'context': story.context
                }
            }
            
            # Get Agile Coach analysis
            agile_response = self._invoke_lambda('AgileCoachFunction', event)
            return self._parse_lambda_response(agile_response, story, AnalysisStatus.AGILE_REVIEW)
            
        except Exception as e:
            print(f"Error in start_analysis: {str(e)}")
            return AnalysisResult(
                original_story=story,
                improved_story=None,
                analysis=str(e),
                suggestions={},
                status=AnalysisStatus.ERROR
            )
    
    def process_user_feedback(self, result: AnalysisResult, approved: bool, edited_story: Optional[Story] = None) -> AnalysisResult:
        """
        Process user feedback and move to next step
        """
        try:
            if not approved and edited_story:
                print(f"\nRestarting with edited story: {edited_story.text}")
                return self.start_analysis(edited_story)
                
            if approved and result.status == AnalysisStatus.AGILE_REVIEW:
                # Get the improved story from the Agile Coach analysis
                story_for_review = result.improved_story if result.improved_story else result.original_story
                print("\nUser approved Agile review.")
                print(f"Original story: {result.original_story.text}")
                print(f"Improved story: {story_for_review.text}")
                print(f"Improved acceptance criteria: {story_for_review.acceptance_criteria}")
                
                # Remove any "Story:" prefix if present
                if story_for_review.text.startswith("Story:"):
                    story_for_review.text = story_for_review.text[6:].strip()
                
                # Remove any "- " prefix from acceptance criteria
                story_for_review.acceptance_criteria = [
                    ac.lstrip("- ").strip() 
                    for ac in story_for_review.acceptance_criteria
                ]
                
                return self.technical_review(story_for_review)
                
            if approved and result.status == AnalysisStatus.TECHNICAL_REVIEW:
                print("\nUser approved Technical review. Analysis complete!")
                result.status = AnalysisStatus.COMPLETE
                return result
                
            print("\nUser rejected without edits")
            return AnalysisResult(
                original_story=result.original_story,
                improved_story=None,
                analysis="User rejected without providing edits",
                suggestions={},
                status=AnalysisStatus.ERROR
            )
            
        except Exception as e:
            print(f"Error in process_user_feedback: {str(e)}")
            return AnalysisResult(
                original_story=result.original_story,
                improved_story=None,
                analysis=str(e),
                suggestions={},
                status=AnalysisStatus.ERROR
            )
    
    def technical_review(self, story: Story) -> AnalysisResult:
        """
        Perform technical review with Senior Dev
        """
        try:
            print(f"\nStarting technical review with story: {story.text}")  # Debug log
            
            event = {
                'body': {
                    'story': story.text,
                    'acceptance_criteria': story.acceptance_criteria,
                    'context': story.context
                }
            }
            
            print(f"Sending event to SeniorDev: {json.dumps(event, indent=2)}")  # Debug log
            
            tech_response = self._invoke_lambda('SeniorDevFunction', event)
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
        """
        Extract improved story from analysis text.
        """
        try:
            print("\nFull analysis text for extraction:")
            print(analysis)  # Debug log
            
            # Look for improved story section in the analysis
            improved_story_marker = "2. Improved version of the story:"
            acceptance_criteria_marker = "3. Enhanced acceptance criteria:"
            
            # Find the sections
            story_start = analysis.find(improved_story_marker)
            if story_start == -1:
                print("No improved story marker found")
                return None
                
            story_start += len(improved_story_marker)
            story_end = analysis.find("4. Questions for clarification:", story_start)
            if story_end == -1:
                story_end = len(analysis)
                
            # Extract and clean the story text
            story_text = analysis[story_start:story_end].strip()
            print(f"\nExtracted story text: {story_text}")
            
            # Extract acceptance criteria
            ac_start = analysis.find(acceptance_criteria_marker)
            acceptance_criteria = []
            if ac_start != -1:
                ac_start += len(acceptance_criteria_marker)
                ac_end = analysis.find("4. Questions for clarification:", ac_start)
                if ac_end == -1:
                    ac_end = len(analysis)
                ac_text = analysis[ac_start:ac_end].strip()
                acceptance_criteria = [
                    criterion.strip('- ').strip()
                    for criterion in ac_text.split('\n')
                    if criterion.strip('- ').strip()
                ]
                print(f"\nExtracted acceptance criteria: {acceptance_criteria}")
            
            return Story(
                text=story_text,
                acceptance_criteria=acceptance_criteria,
                context=original_story.context,
                version=original_story.version + 1
            )
            
        except Exception as e:
            print(f"Error extracting improved story: {str(e)}")
            return None 
from fastapi import APIRouter, HTTPException
from ai.shared.story_analyzer import StoryAnalyzer, Story, AnalysisResult
from pydantic import BaseModel
from typing import Dict, Any
from ai.workflow.story_handler_days import handle_story_workflow_days

router = APIRouter()

class FeedbackRequest(BaseModel):
    analysis_result: Dict[str, Any]
    approved: bool

class EstimationRequest(BaseModel):
    story: Story  # Using the Story model from story_analyzer

@router.post("/analyze")
async def analyze_story(story: Story) -> AnalysisResult:
    try:
        analyzer = StoryAnalyzer()
        result = analyzer.start_analysis(story)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/feedback")
async def process_feedback(request: FeedbackRequest) -> Dict[str, Any]:
    try:
        analyzer = StoryAnalyzer()
        result = analyzer.process_user_feedback(
            request.analysis_result,
            request.approved
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/estimate/days")
async def estimate_days(request: EstimationRequest):
    try:
        print(f"Received story: {request.story}")  # Debug
        print(f"Story type: {type(request.story)}")  # Debug
        
        # Try both ways:
        try:
            story_dict = request.story.dict()
            print(f"Using .dict(): {story_dict}")  # Debug
        except:
            story_dict = {
                "text": request.story.text,
                "acceptance_criteria": request.story.acceptance_criteria,
                "context": request.story.context,
                "version": request.story.version
            }
            print(f"Using manual dict: {story_dict}")  # Debug
        
        result = handle_story_workflow_days(
            story=story_dict,
            step="technical_feedback",
            action="approve"
        )
        return result
    except Exception as e:
        print(f"Error in estimate_days: {str(e)}")  # Debug
        raise HTTPException(status_code=500, detail=str(e)) 
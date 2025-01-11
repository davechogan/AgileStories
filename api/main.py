from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

print("Attempting to import story_handler_days...")
from ai.workflow.story_handler_days import handle_story_workflow_days
print("Successfully imported story_handler_days")

print("Attempting to import story_analyzer...")
from ai.shared.story_analyzer import StoryAnalyzer
print("Successfully imported story_analyzer")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Story(BaseModel):
    text: str
    acceptance_criteria: List[str]
    context: Optional[str] = ""
    version: int

class AnalysisFeedback(BaseModel):
    analysis_result: Dict[str, Any]
    approved: bool

class EstimationRequest(BaseModel):
    story: Story

@app.post("/api/analyze")
async def analyze_story(story: Story):
    try:
        analyzer = StoryAnalyzer()
        result = analyzer.start_analysis(story.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/feedback")
async def process_feedback(feedback: AnalysisFeedback):
    try:
        analyzer = StoryAnalyzer()
        result = analyzer.process_user_feedback(
            feedback.analysis_result,
            feedback.approved
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/estimate/days")
async def estimate_days(request: EstimationRequest):
    try:
        result = handle_story_workflow_days(
            story=request.story.dict(),
            step="technical_feedback",
            action="approve"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
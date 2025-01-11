import os
import sys
import json
import openai
import concurrent.futures
from typing import Dict, List, Any

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ai.shared.story_analyzer import StoryAnalyzer
from ai.agents.team.senior_dev_lead import SeniorDevLead
from ai.agents.team.senior_dev import SeniorDev
from ai.agents.team.mid_dev import MidDev
from ai.agents.team.junior_dev import JuniorDev
from ai.agents.team.grad_dev import GradDev
from ai.agents.team.senior_qa import SeniorQA
from ai.agents.team.junior_qa import JuniorQA
from ai.agents.team.ux_designer import UXDesigner

def get_team_day_estimates(story_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get person-day estimates from all team members and calculate average"""
    print("Starting team estimation...")  # Debug
    
    # Set up OpenAI credentials from project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_json_path = os.path.join(project_root, 'env.json')
    print(f"Looking for env.json at: {env_json_path}")  # Debug
    
    with open(env_json_path, 'r') as f:
        env_vars = json.load(f)
        openai.api_key = env_vars['SeniorDevFunction']['OPENAI_API_KEY']
        openai.organization = env_vars['SeniorDevFunction']['OPENAI_ORG_ID']
    
    # Create team members
    team = [
        SeniorDevLead(),
        SeniorDev(),
        MidDev(),
        JuniorDev(),
        GradDev(),
        SeniorQA(),
        JuniorQA(),
        UXDesigner()
    ]
    
    # Format event for estimation
    test_event = {
        'body': {
            'story': story_data['text'],
            'acceptance_criteria': story_data['acceptance_criteria'],
            'context': story_data.get('context', '')
        }
    }
    
    # Get estimates in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # Start all estimation tasks
        future_to_member = {
            executor.submit(member.estimate_effort, test_event): member 
            for member in team
        }
        
        # Process responses as they complete
        responses = []
        for future in concurrent.futures.as_completed(future_to_member):
            member = future_to_member[future]
            try:
                response = future.result()
                if response['statusCode'] == 200:
                    body = json.loads(response['body'])
                    responses.append({
                        'name': member.name,
                        'role': member.role,
                        'estimate': extract_day_estimate(body['analysis']),
                        'justification': body['analysis']
                    })
            except Exception as e:
                print(f"\nError getting estimate from {member.name}: {e}")
    
    # Calculate average
    estimates = [r['estimate'] for r in responses if r['estimate'] is not None]
    average = sum(estimates) / len(estimates) if estimates else 0
    
    return {
        'team_estimates': responses,
        'average': round(average, 1),
        'total_estimates': len(estimates)
    }

def extract_day_estimate(analysis: str) -> float:
    """Extract person-days estimate from analysis text"""
    for line in analysis.split('\n'):
        if 'Person-days:' in line:
            try:
                return float(line.split(':')[1].strip())
            except Exception:
                pass
    return None

def handle_story_workflow_days(story: Dict[str, Any], step: str, action: str) -> Dict[str, Any]:
    """
    Handle the story workflow steps with person-day estimates:
    - Initial Analysis (Agile Coach)
    - Technical Review
    - Team Day Estimation
    """
    analyzer = StoryAnalyzer()
    
    if step == "start":
        return analyzer.start_analysis(story)
    
    elif step == "agile_feedback":
        return analyzer.process_user_feedback(story, action == "approve")
        
    elif step == "technical_feedback" and action == "approve":
        return get_team_day_estimates(story)
    
    return {"error": "Invalid step or action"} 
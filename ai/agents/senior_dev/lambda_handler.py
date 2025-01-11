import os
import json
from typing import Dict, Any
import openai
from dotenv import load_dotenv
from pathlib import Path

SENIOR_DEV_PROMPT = """You are an experienced Senior Developer reviewing user stories.
Given the following user story and acceptance criteria, please review it for technical feasibility and implementation details:

Story: {story}

Current Acceptance Criteria:
{acceptance_criteria}

Context: {context}

Please provide your response in the following format:

Technical Analysis:
- Feasibility: [High/Medium/Low]
- Complexity: [High/Medium/Low]
- Dependencies: [List required systems/services]
- Technical Risks: [List potential challenges]

Improved version of the story:
[If technical clarifications are needed, write the improved story here]

Enhanced acceptance criteria:
[List technically-enhanced criteria, each on a new line with a hyphen]

Implementation Details:
- Architecture: [Key components]
- Data Flow: [Data handling details]
- Security: [Security considerations]
- Testing: [Testing approach]"""

def get_openai_key():
    """Get OpenAI key from env.json"""
    try:
        # Get project root (similar to test_feedback.py)
        project_root = Path(__file__).parents[3].absolute()
        env_path = project_root / 'env.json'
        print(f"Looking for env.json at: {env_path}")
        
        with open(env_path) as f:
            env_vars = json.load(f)
            return env_vars['SeniorDevFunction']['OPENAI_API_KEY']
    except Exception as e:
        print(f"Error reading env.json: {e}")
        return None

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for Senior Dev analysis
    """
    try:
        print("SeniorDev Lambda started")
        print(f"Event received: {json.dumps(event, indent=2)}")
        
        # Configure OpenAI directly from file
        openai.api_key = get_openai_key()
        print(f"OpenAI Key loaded: {bool(openai.api_key)}")
        
        # Get the story details from the event body
        if isinstance(event.get('body'), str):
            body = json.loads(event.get('body', '{}'))
        else:
            body = event.get('body', {})
            
        print(f"Parsed body: {json.dumps(body, indent=2)}")
        
        story_text = body.get('story', '')
        acceptance_criteria = body.get('acceptance_criteria', [])
        context = body.get('context', '')
        
        if not story_text:
            print("No story text provided")
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'No story provided',
                    'status': 'error'
                })
            }
        
        if not openai.api_key:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'OpenAI API key not found in env.json',
                    'status': 'error'
                })
            }
        
        print("Making OpenAI API call...")
        
        # Create the analysis
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an experienced Senior Developer."},
                {"role": "user", "content": SENIOR_DEV_PROMPT.format(
                    story=story_text,
                    acceptance_criteria="\n".join(f"- {ac}" for ac in acceptance_criteria),
                    context=context
                )}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        analysis = response.choices[0].message.content
        print(f"OpenAI Response: {analysis}")
        
        # Return the analysis in the correct format
        return {
            'statusCode': 200,
            'body': json.dumps({
                'analysis': analysis,
                'suggestions': {},
                'status': 'success'
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"Lambda handler error: {str(e)}")
        import traceback
        print(f"Full traceback:\n{traceback.format_exc()}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'status': 'error'
            })
        }
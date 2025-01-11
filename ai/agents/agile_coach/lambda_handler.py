import os
import json
from typing import Dict, Any
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI with API key
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.organization = os.getenv('OPENAI_ORG_ID')

# Define our base prompt template
AGILE_COACH_PROMPT = """You are an experienced Agile Coach helping to improve user stories.
Given the following user story and acceptance criteria, please analyze and improve it based on INVEST criteria:

Story: {story}

Current Acceptance Criteria:
{acceptance_criteria}

Context: {context}

Please provide your response in the following format:

INVEST Analysis:
- Independent: [analysis]
- Negotiable: [analysis]
- Valuable: [analysis]
- Estimable: [analysis]
- Small: [analysis]
- Testable: [analysis]

Improved Story:
[Write the improved user story here, maintaining the "As a/I want/So that" format]

Enhanced Acceptance Criteria:
[List each criterion on a new line, starting with a hyphen]

Additional Suggestions:
[Any other recommendations or questions for clarification]

Please ensure the improved story and acceptance criteria sections are clearly marked as they will be automatically extracted."""

def analyze_story(story_text: str, acceptance_criteria: list, context: str) -> Dict[str, Any]:
    """
    Analyze and improve a user story using OpenAI's GPT model.
    """
    try:
        # Format acceptance criteria for the prompt
        formatted_ac = "\n".join(f"- {ac}" for ac in acceptance_criteria) if acceptance_criteria else "None provided"
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an experienced Agile Coach, with 10 years of experience leading scrum teams as a scrum master."},
                {"role": "user", "content": AGILE_COACH_PROMPT.format(
                    story=story_text,
                    acceptance_criteria=formatted_ac,
                    context=context
                )}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract the response content
        analysis = response.choices[0].message.content
        
        return {
            'analysis': analysis,
            'original_story': story_text,
            'original_acceptance_criteria': acceptance_criteria,
            'context': context,
            'status': 'success'
        }
        
    except Exception as e:
        print(f"Error in analyze_story: {str(e)}")  # Debug logging
        return {
            'error': str(e),
            'status': 'error'
        }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for Agile Coach analysis
    """
    try:
        print("AgileCoach Lambda started")
        print(f"Event received: {json.dumps(event, indent=2)}")
        
        # Debug environment variables
        print(f"OpenAI Key exists: {bool(os.getenv('OPENAI_API_KEY'))}")
        print(f"OpenAI Org exists: {bool(os.getenv('OPENAI_ORG_ID'))}")
        
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
        
        # Configure OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        openai.organization = os.getenv('OPENAI_ORG_ID')
        
        print("Making OpenAI API call...")
        print(f"Using prompt template:\n{AGILE_COACH_PROMPT}")
        
        formatted_prompt = AGILE_COACH_PROMPT.format(
            story=story_text,
            acceptance_criteria="\n".join(f"- {ac}" for ac in acceptance_criteria),
            context=context
        )
        print(f"Formatted prompt:\n{formatted_prompt}")
        
        # Create the analysis
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an experienced Agile Coach."},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        analysis = response.choices[0].message.content
        print(f"OpenAI Response: {analysis}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'analysis': analysis,
                'suggestions': {},
                'status': 'success'
            })
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

if __name__ == '__main__':
    # Local testing
    test_event = {
        'body': json.dumps({
            'story': 'As a product owner, I want to create better user stories'
        })
    }
    print(json.dumps(lambda_handler(test_event, None), indent=2)) 
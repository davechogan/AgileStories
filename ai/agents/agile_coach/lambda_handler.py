import os
import json
from typing import Dict, Any
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
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

Please provide:
1. Analysis of current story (focusing on INVEST principles)
2. Improved version of the story
3. Enhanced acceptance criteria
4. Questions for clarification (if needed)

Focus on making the story Independent, Negotiable, Valuable, Estimable, Small, and Testable."""

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
                {"role": "system", "content": "You are an experienced Agile Coach."},
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
    AWS Lambda handler for story analysis.
    """
    try:
        # Get the story and acceptance criteria from the event body
        body = event.get('body', {})
        story_text = body.get('story', '')
        acceptance_criteria = body.get('acceptance_criteria', [])
        context_text = body.get('context', 'No context provided')
        
        print(f"Received story: {story_text}")  # Debug logging
        print(f"Acceptance criteria: {acceptance_criteria}")  # Debug logging
        print(f"Context: {context_text}")  # Debug logging
        
        if not story_text:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'No story provided',
                    'status': 'error'
                })
            }
        
        # Analyze the story
        result = analyze_story(story_text, acceptance_criteria, context_text)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        print(f"Lambda handler error: {str(e)}")  # Debug logging
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
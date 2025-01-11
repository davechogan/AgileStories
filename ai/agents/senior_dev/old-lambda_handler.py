import os
import json
from typing import Dict, Any
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define our base prompt template
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

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        print("\n=== Senior Dev Lambda Started ===")
        print(f"Event received: {json.dumps(event, indent=2)}")
        
        # Get the story details from the event body
        if isinstance(event.get('body'), str):
            body = json.loads(event.get('body', '{}'))
        else:
            body = event.get('body', {})
            
        story_text = body.get('story', '')
        acceptance_criteria = body.get('acceptance_criteria', [])
        context = body.get('context', '')
        
        print(f"\nStory Text: {story_text}")
        print(f"\nAcceptance Criteria: {json.dumps(acceptance_criteria, indent=2)}")
        
        # Configure OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        openai.organization = os.getenv('OPENAI_ORG_ID')
        
        print("\nMaking OpenAI API call...")
        print(f"OpenAI Key exists: {bool(openai.api_key)}")
        print(f"OpenAI Org exists: {bool(openai.organization)}")
        
        # Format acceptance criteria for prompt
        formatted_ac = "\n".join(f"- {ac}" for ac in acceptance_criteria)
        
        # Create the analysis
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an experienced Senior Developer."},
                {"role": "user", "content": SENIOR_DEV_PROMPT.format(
                    story=story_text,
                    acceptance_criteria=formatted_ac,
                    context=context
                )}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        analysis = response.choices[0].message.content
        print(f"\nOpenAI Response: {analysis}")
        
        # Return the actual analysis
        return {
            'statusCode': 200,
            'body': json.dumps({
                'analysis': analysis,
                'suggestions': {},
                'status': 'success'
            })
        }
        
    except Exception as e:
        print(f"\nLambda handler error: {str(e)}")
        import traceback
        print(f"Full traceback:\n{traceback.format_exc()}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'status': 'error'
            })
        }

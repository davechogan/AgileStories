import json
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from ai.agents.senior_dev.lambda_handler import lambda_handler

def test_senior_dev():
    """Test the Senior Dev Lambda handler directly"""
    # Load test event
    with open('events/test-senior-dev.json', 'r') as f:
        test_event = json.load(f)
    
    print("\nTest Event:")
    print(json.dumps(test_event, indent=2))
    
    # Call Lambda handler directly
    print("\nCalling Senior Dev Lambda handler...")
    response = lambda_handler(test_event, None)
    
    print("\n=== Lambda Response ===")
    print("Full response:")
    print(json.dumps(response, indent=2))
    
    if 'body' in response:
        body = response['body']
        if isinstance(body, str):
            body = json.loads(body)
            
        print("\n=== Analysis ===")
        print(body.get('analysis', 'No analysis found'))
        print("\n=== Status ===")
        print(body.get('status', 'No status found'))

if __name__ == "__main__":
    test_senior_dev() 
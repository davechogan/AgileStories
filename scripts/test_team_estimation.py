import os
import sys
import json
from dotenv import load_dotenv
import openai

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

def load_env_vars():
    """Load environment variables from env.json or .env"""
    try:
        # First try env.json
        with open('env.json', 'r') as f:
            env_vars = json.load(f)
            openai.api_key = env_vars['SeniorDevFunction']['OPENAI_API_KEY']
            openai.organization = env_vars['SeniorDevFunction']['OPENAI_ORG_ID']
            print("Loaded credentials from env.json")
    except Exception as e:
        print(f"Could not load from env.json: {e}")
        # Try .env as fallback
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        openai.organization = os.getenv('OPENAI_ORG_ID')
        if openai.api_key and openai.organization:
            print("Loaded credentials from .env")
        else:
            print("Failed to load OpenAI credentials")
            sys.exit(1)

from ai.agents.team.senior_dev_lead import SeniorDevLead
from ai.agents.team.senior_dev import SeniorDev
from ai.agents.team.mid_dev import MidDev
from ai.agents.team.junior_dev import JuniorDev
from ai.agents.team.grad_dev import GradDev
from ai.agents.team.senior_qa import SeniorQA
from ai.agents.team.junior_qa import JuniorQA

def print_estimate(response):
    """Pretty print a team member's estimate"""
    if response['statusCode'] == 200:
        body = json.loads(response['body'])
        member = body['team_member']
        print(f"\n=== {member['name']} ({member['role']}) ===")
        print(f"Experience: {member['experience']} years")
        print("\nAnalysis:")
        print(body['analysis'])
        print("\nRaw Response:")
        print(json.dumps(body, indent=2))  # Show the complete response structure
        print("="*80)
    else:
        print(f"\nError: {response.get('body', 'Unknown error')}")

def calculate_average_estimate(responses):
    """Calculate average estimate from all team members"""
    estimates = []
    for response in responses:
        if response['statusCode'] == 200:
            body = json.loads(response['body'])
            member = body['team_member']
            analysis = body['analysis']
            
            print(f"\nDEBUG: Parsing estimate for {member['name']}")
            # Print each line containing 'Person-days'
            for line in analysis.split('\n'):
                if 'Person-days' in line:
                    print(f"Found line: '{line}'")
                    try:
                        # Extract number after the colon
                        estimate = float(line.split(':')[1].strip())
                        estimates.append(estimate)
                        print(f"Successfully parsed estimate: {estimate}")
                        break
                    except Exception as e:
                        print(f"Error parsing line: {e}")
            
    if estimates:
        avg = sum(estimates) / len(estimates)
        print(f"\n=== Team Average Estimate ===")
        print(f"Average: {avg:.1f} person-days")
        print(f"Individual estimates: {estimates}")
        print(f"Based on {len(estimates)} estimates")
        print("="*80)
    else:
        print("\nNo valid estimates found")

def main():
    # Load environment variables first
    load_env_vars()
    
    # Test story from Senior Dev analysis
    test_event = {
        'body': {
            'story': "As a unified platform user, I want the ability to set up a daily schedule that reoccurs every 1 to 6 days so that I can manage my tasks efficiently.",
            'acceptance_criteria': [
                "The user can select 'Daily' as the 'Interval' when creating or editing a schedule.",
                "The user can set 'Recur Every' to a number between '1' and '6' when 'Interval' is set to 'Daily'.",
                "The system prevents the user from setting 'Recur Every' to a number outside the range of '1' to '6' when 'Interval' is set to 'Daily'.",
                "The user receives an appropriate error message when attempting to set 'Recur Every' to a number outside the range of '1' to '6' when 'Interval' is set to 'Daily'.",
                "The schedule correctly recurs every 'n' days, where 'n' is between '1' and '6', when 'Recur Every' is set to 'n' and 'Interval' is set to 'Daily'."
            ],
            'context': """Technical Analysis:
- Feasibility: High
- Complexity: Medium
- Dependencies: Task management system, scheduling service, user interface for schedule creation / editing, error handling mechanism, database service for storing schedules
- Technical Risks: Potential challenges may arise in implementing the repeat functionality in the scheduling service, handling edge cases related to time zones, and ensuring that the system handles invalid inputs gracefully

Implementation Details:
- Architecture: Key components include a user interface for schedule creation / editing, a backend service for handling scheduling logic, and a database for storing schedules.
- Data Flow: The user inputs are validated on the client side and then sent to the server. The server processes the request, interacts with the database to store the schedule, and sends a response back to the client.
- Security: User authentication should be in place to ensure that only authorized users can create or edit schedules. Input validation should be done both on the client and server side to prevent SQL injection or other security threats.
- Testing: Unit tests should be written for all core functionality. Integration tests should test the interaction between the client, server, and database. End-to-end tests should be performed to ensure that the scheduling feature works as expected from a user's perspective."""
        }
    }
    
    # Create team members
    team = [
        SeniorDevLead(),
        SeniorDev(),
        MidDev(),
        JuniorDev(),
        GradDev(),
        SeniorQA(),
        JuniorQA()
    ]
    
    # Get estimates from each team member
    responses = []
    print("\nGathering team estimates...")
    for member in team:
        response = member.estimate_effort(test_event)
        responses.append(response)
        print_estimate(response)
    
    # Calculate and show average estimate
    calculate_average_estimate(responses)

if __name__ == "__main__":
    main() 
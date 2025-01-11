from .base_estimator import BaseTeamMemberPoints

class JuniorQAPoints(BaseTeamMemberPoints):
    """Junior QA Analyst with 1.5 years experience - Points Estimator"""
    
    def __init__(self):
        super().__init__(
            name="Jamie Lee",
            role="Junior QA Analyst",
            experience_years=1.5
        )
    
    def get_prompt(self, story: str, acceptance_criteria: list, context: str) -> str:
        return f"""As a Junior QA Analyst, analyze this user story and provide a story point estimate using the Fibonacci sequence.

Story:
{story}

Acceptance Criteria:
{chr(10).join(f'- {ac}' for ac in acceptance_criteria)}

Context:
{context}

Consider:
- Time to understand testing requirements
- Manual test case creation
- Basic test automation needs
- Functional testing coverage
- Learning curve for tools
- Documentation time
- Support needed from senior QA

Please provide your response in the following format:

Story Points: [Choose from: 1, 2, 3, 5, 8, 13, 21]
Confidence Level: [High/Medium/Low]

Testing Considerations:
[List key testing aspects affecting the estimate]

Risk Factors:
[List potential testing challenges]

Explanation:
[Brief justification of your story points estimate]""" 
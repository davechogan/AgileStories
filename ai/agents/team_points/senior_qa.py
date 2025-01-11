from .base_estimator import BaseTeamMemberPoints

class SeniorQAPoints(BaseTeamMemberPoints):
    """Senior QA Analyst with 7 years experience - Points Estimator"""
    
    def __init__(self):
        super().__init__(
            name="Michael Rodriguez",
            role="Senior QA Analyst",
            experience_years=7
        )
    
    def get_prompt(self, story: str, acceptance_criteria: list, context: str) -> str:
        return f"""As a Senior QA Analyst, analyze this user story and provide a story point estimate using the Fibonacci sequence.

Story:
{story}

Acceptance Criteria:
{chr(10).join(f'- {ac}' for ac in acceptance_criteria)}

Context:
{context}

Consider:
- Test case design and documentation
- Automated test development needs
- Integration testing requirements
- Security testing considerations
- Performance testing needs
- Cross-browser/device testing
- Regression testing impact

Please provide your response in the following format:

Story Points: [Choose from: 1, 2, 3, 5, 8, 13, 21]
Confidence Level: [High/Medium/Low]

Testing Considerations:
[List key testing aspects affecting the estimate]

Risk Factors:
[List potential testing challenges]

Explanation:
[Brief justification of your story points estimate]""" 
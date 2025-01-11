from .base_estimator import BaseTeamMemberPoints

class SeniorDevPoints(BaseTeamMemberPoints):
    """Senior Developer with 8 years experience - Points Estimator"""
    
    def __init__(self):
        super().__init__(
            name="Alex Thompson",
            role="Senior Developer",
            experience_years=8
        )
    
    def get_prompt(self, story: str, acceptance_criteria: list, context: str) -> str:
        return f"""As a Senior Developer, analyze this user story and provide a story point estimate using the Fibonacci sequence.

Story:
{story}

Acceptance Criteria:
{chr(10).join(f'- {ac}' for ac in acceptance_criteria)}

Context:
{context}

Consider:
- Implementation complexity
- Required architectural changes
- Integration requirements
- Performance implications
- Security considerations
- Testing support needed

Please provide your response in the following format:

Story Points: [Choose from: 1, 2, 3, 5, 8, 13, 21]
Confidence Level: [High/Medium/Low]

Technical Considerations:
[List key technical factors affecting the estimate]

Risk Factors:
[List potential risks that could impact complexity]

Explanation:
[Brief justification of your story points estimate]""" 
from .base_estimator import BaseTeamMemberPoints

class MidDevPoints(BaseTeamMemberPoints):
    """Mid-level Developer with 4 years experience - Points Estimator"""
    
    def __init__(self):
        super().__init__(
            name="Emily Parker",
            role="Mid-level Developer",
            experience_years=4
        )
    
    def get_prompt(self, story: str, acceptance_criteria: list, context: str) -> str:
        return f"""As a Mid-level Developer, analyze this user story and provide a story point estimate using the Fibonacci sequence.

Story:
{story}

Acceptance Criteria:
{chr(10).join(f'- {ac}' for ac in acceptance_criteria)}

Context:
{context}

Consider:
- Implementation requirements
- Code changes needed
- Testing requirements
- Documentation updates
- Potential challenges
- Learning curve for new technologies

Please provide your response in the following format:

Story Points: [Choose from: 1, 2, 3, 5, 8, 13, 21]
Confidence Level: [High/Medium/Low]

Technical Considerations:
[List key technical factors affecting the estimate]

Risk Factors:
[List potential risks that could impact complexity]

Explanation:
[Brief justification of your story points estimate]""" 
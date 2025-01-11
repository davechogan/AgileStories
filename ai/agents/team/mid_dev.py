from .base_estimator import BaseTeamMember

class MidDev(BaseTeamMember):
    """Mid-level Developer with 3-5 years experience"""
    
    def __init__(self):
        super().__init__(
            name="Emily Parker",
            role="Mid-level Developer",
            experience_years=4
        )
    
    def get_prompt(self, story: str, acceptance_criteria: list, context: str) -> str:
        return f"""As a Mid-level Developer with {self.experience_years} years of experience, 
please analyze this user story and provide an effort estimate in person-days.

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

Effort Estimate:
- Person-days: [X.X]
- Confidence Level: [High/Medium/Low]

Technical Considerations:
[List key technical factors affecting the estimate]

Risk Factors:
[List potential risks that could impact the timeline]

Explanation:
[Brief justification of your estimate]""" 
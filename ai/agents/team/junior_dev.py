from .base_estimator import BaseTeamMember

class JuniorDev(BaseTeamMember):
    """Junior Developer with 1-2 years experience"""
    
    def __init__(self):
        super().__init__(
            name="Ryan Foster",
            role="Junior Developer",
            experience_years=2
        )
    
    def get_prompt(self, story: str, acceptance_criteria: list, context: str) -> str:
        return f"""As a Junior Developer with {self.experience_years} years of experience, 
please analyze this user story and provide an effort estimate in person-days.

Story:
{story}

Acceptance Criteria:
{chr(10).join(f'- {ac}' for ac in acceptance_criteria)}

Context:
{context}

Consider:
- Your current skill level
- Time needed to understand requirements
- Research and learning time
- Implementation time
- Testing and documentation
- Time for questions and guidance

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
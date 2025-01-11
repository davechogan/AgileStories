from .base_estimator import BaseTeamMember

class GradDev(BaseTeamMember):
    """Graduate Developer with <1 year experience"""
    
    def __init__(self):
        super().__init__(
            name="Zoe Williams",
            role="Graduate Developer",
            experience_years=0.5
        )
    
    def get_prompt(self, story: str, acceptance_criteria: list, context: str) -> str:
        return f"""As a Graduate Developer with {self.experience_years} years of experience, 
please analyze this user story and provide an effort estimate in person-days.

Story:
{story}

Acceptance Criteria:
{chr(10).join(f'- {ac}' for ac in acceptance_criteria)}

Context:
{context}

Consider:
- Your limited experience with the codebase
- Time needed to understand the requirements fully
- Research and learning curve
- Pair programming needs
- Code review iterations
- Documentation reading time
- Questions and mentoring needs

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
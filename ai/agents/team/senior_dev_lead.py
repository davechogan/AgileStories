from .base_estimator import BaseTeamMember

class SeniorDevLead(BaseTeamMember):
    """Senior Developer Lead with 10+ years experience"""
    
    def __init__(self):
        super().__init__(
            name="Sarah Chen",
            role="Senior Developer Lead",
            experience_years=12
        )
    
    def get_prompt(self, story: str, acceptance_criteria: list, context: str) -> str:
        return f"""As a Senior Developer Lead with {self.experience_years} years of experience, 
please analyze this user story and provide an effort estimate in person-days.

Story:
{story}

Acceptance Criteria:
{chr(10).join(f'- {ac}' for ac in acceptance_criteria)}

Context:
{context}

Consider:
- Technical complexity and architecture implications
- Team coordination needs
- Code review and mentoring time
- Integration points and dependencies
- Technical debt implications
- Security considerations

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
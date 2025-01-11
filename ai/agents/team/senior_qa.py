from .base_estimator import BaseTeamMember

class SeniorQA(BaseTeamMember):
    """Senior QA Analyst with 5+ years experience"""
    
    def __init__(self):
        super().__init__(
            name="Michael Rodriguez",
            role="Senior QA Analyst",
            experience_years=7
        )
    
    def get_prompt(self, story: str, acceptance_criteria: list, context: str) -> str:
        return f"""As a Senior QA Analyst with {self.experience_years} years of experience, 
please analyze this user story and provide a testing effort estimate in person-days.

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

Effort Estimate:
- Person-days: [X.X]
- Confidence Level: [High/Medium/Low]

Testing Considerations:
[List key testing aspects affecting the estimate]

Risk Factors:
[List potential testing challenges]

Explanation:
[Brief justification of your estimate]""" 
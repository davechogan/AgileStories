from .base_estimator import BaseTeamMemberPoints

class GradDevPoints(BaseTeamMemberPoints):
    """Graduate Developer with <1 year experience - Points Estimator"""
    
    def __init__(self):
        super().__init__(
            name="Zoe Williams",
            role="Graduate Developer",
            experience_years=0.5
        )
    
    def get_prompt(self, story: str, acceptance_criteria: list, context: str) -> str:
        return f"""As a Graduate Developer, analyze this user story and provide a story point estimate using the Fibonacci sequence.

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

Story Points: [Choose from: 1, 2, 3, 5, 8, 13, 21]
Confidence Level: [High/Medium/Low]

Technical Considerations:
[List key technical factors affecting the estimate]

Risk Factors:
[List potential risks that could impact complexity]

Explanation:
[Brief justification of your story points estimate]""" 
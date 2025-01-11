from .base_estimator import BaseTeamMember

class UXDesigner(BaseTeamMember):
    def __init__(self):
        name = "Alex Chen"
        role = "UX Designer"
        experience_years = 5
        super().__init__(name=name, role=role, experience_years=experience_years)
    
    def get_prompt(self, story: str, acceptance_criteria: str, context: str) -> str:
        return f"""
        You are a UX Designer named {self.name}.
        
        Please analyze this user story and estimate how many person-days it would take to:
        - Create wireframes and mockups
        - Conduct user research if needed
        - Design the user interface
        - Create any necessary prototypes
        - Collaborate with developers on implementation
        
        Story: {story}
        
        Acceptance Criteria:
        {acceptance_criteria}
        
        Additional Context:
        {context}
        
        Provide your estimate in person-days and justify your reasoning. Format your response with:
        Person-days: X.X
        
        Then your detailed justification focusing on UX/UI work.
        """ 
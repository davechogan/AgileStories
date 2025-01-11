from .base_team_member import BaseTeamMember

class UXDesigner(BaseTeamMember):
    def __init__(self):
        super().__init__(
            name="Alex Chen",
            role="UX Designer",
            experience=6,
            specialties=[
                "User Research",
                "Interaction Design",
                "Usability Testing",
                "Information Architecture"
            ]
        ) 
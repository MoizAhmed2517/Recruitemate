from pydantic import BaseModel
from typing import List, Optional

class SocialLinks(BaseModel):
    LinkedIn: Optional[str] = None
    GitHub: Optional[str] = None

class WorkHistory(BaseModel):
    Company: str
    Position: str
    Duration: str
    Key_Achievements: str

class Education(BaseModel):
    Degree: str
    Institution: str
    Duration: str

class CVOutputModel(BaseModel):
    social_links: SocialLinks
    Professional_Summary: str
    Technical_Skills: List[str]
    Work_History: List[WorkHistory]
    Total_Experience: int
    Education: List[Education]
    Key_Achievements: List[str]
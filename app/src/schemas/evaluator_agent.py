from pydantic import BaseModel
from typing import List
from src.schemas.cv_reader_agent import SocialLinks, Education

class ScoreBreakdown(BaseModel):
    Experience: str
    Skills: str
    Responsibilities: str
    Requirements: str
    Softskills: str

class MatchOutputModel(BaseModel):
    social_links: SocialLinks
    Technical_Skills: List[str]
    Total_Experience: int
    Education: List[Education]
    Candidate_Summary: str
    Score_Breakdown: ScoreBreakdown
    CV_Score: str
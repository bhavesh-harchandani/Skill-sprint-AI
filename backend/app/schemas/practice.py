from pydantic import BaseModel
from typing import List, Optional

class PracticeItemBase(BaseModel):
    title: str
    domain: str
    topic: str
    difficulty: str
    link: str
    description: str
    tags: Optional[List[str]] = []

class PracticeItemCreate(PracticeItemBase):
    pass

class PracticeItemResponse(PracticeItemBase):
    id: int
    
    class Config:
        from_attributes = True

class RecommendationResponse(BaseModel):
    week_id: int
    focus: str
    topics: List[str]
    domain: str
    recommendations: List[PracticeItemResponse]

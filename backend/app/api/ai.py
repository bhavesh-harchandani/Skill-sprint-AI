from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.openai_service import generate_clarifying_questions, generate_roadmap
from app.services.domain_detector import detect_domain_with_ai
from app.schemas.ai import GenerateRoadmapRequest, GenerateRoadmapResponse
from app.crud import roadmap as roadmap_crud
from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["ai"])

class ClarifyRequest(BaseModel):
    goal: str

class ClarifyResponse(BaseModel):
    questions: list[str]

@router.post("/clarify", response_model=ClarifyResponse)
async def clarify_goal(request: ClarifyRequest):
    """Generate clarifying questions for a learning goal"""
    if not request.goal or len(request.goal.strip()) < 3:
        raise HTTPException(status_code=400, detail="Goal must be at least 3 characters")
    
    try:
        questions = await generate_clarifying_questions(request.goal)
        return ClarifyResponse(questions=questions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")

@router.post("/generate-roadmap", response_model=GenerateRoadmapResponse)
async def generate_roadmap_endpoint(
    request: GenerateRoadmapRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate AI-powered roadmap and save to database"""
    if not request.goal or len(request.goal.strip()) < 3:
        raise HTTPException(status_code=400, detail="Goal must be at least 3 characters")
    
    if request.duration_weeks < 1 or request.duration_weeks > 52:
        raise HTTPException(status_code=400, detail="Duration must be between 1 and 52 weeks")
    
    try:
        # Detect domain using AI
        logger.info(f"Detecting domain for goal: {request.goal}")
        domain = detect_domain_with_ai(request.goal)
        logger.info(f"Detected domain: {domain}")
        
        # Generate roadmap using OpenAI
        generated = await generate_roadmap(request.goal, request.answers, request.duration_weeks)
        
        # Save to database with user_id and detected domain
        db_roadmap = roadmap_crud.create_roadmap_from_ai(db, request.goal, generated, current_user.id, domain)
        
        # Format response
        return GenerateRoadmapResponse(
            roadmap_id=db_roadmap.id,
            title=generated.title,
            goal=request.goal,
            duration_weeks=generated.duration_weeks,
            weeks=generated.weeks
        )
        
    except Exception as e:
        logger.error(f"Failed to generate roadmap: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate roadmap: {str(e)}")

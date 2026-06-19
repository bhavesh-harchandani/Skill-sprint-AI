from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.weekplan import WeekPlan
from app.schemas.progress import WeekCompleteResponse
from app.crud import progress as progress_crud

router = APIRouter(prefix="/weeks", tags=["weeks"])

@router.patch("/{week_id}/complete", response_model=WeekCompleteResponse)
def toggle_week_completion(
    week_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle completion status for a week"""
    # Verify week belongs to user's roadmap (eagerly load roadmap)
    week = db.query(WeekPlan).options(joinedload(WeekPlan.roadmap)).filter(WeekPlan.id == week_id).first()
    if not week:
        raise HTTPException(status_code=404, detail="Week not found")
    
    # Access roadmap to ensure it's loaded
    roadmap = week.roadmap
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    if roadmap.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this week")
    
    try:
        result = progress_crud.toggle_week_completion(db, week_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update progress: {str(e)}")

@router.get("/{week_id}/status")
def get_week_status(
    week_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get completion status for a specific week"""
    # Verify week belongs to user's roadmap (eagerly load roadmap)
    week = db.query(WeekPlan).options(joinedload(WeekPlan.roadmap)).filter(WeekPlan.id == week_id).first()
    if not week:
        raise HTTPException(status_code=404, detail="Week not found")
    
    # Access roadmap to ensure it's loaded
    roadmap = week.roadmap
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    if roadmap.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this week")
    
    try:
        status = progress_crud.get_week_status(db, week_id)
        return status
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.roadmap import RoadmapResponse
from app.models.roadmap import Roadmap

router = APIRouter(prefix="/share", tags=["share"])

@router.get("/{public_id}", response_model=RoadmapResponse)
def get_shared_roadmap(public_id: str, db: Session = Depends(get_db)):
    """Get a roadmap by public share ID (read-only)"""
    db_roadmap = db.query(Roadmap).filter(Roadmap.public_id == public_id).first()
    
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Shared roadmap not found")
    
    return db_roadmap

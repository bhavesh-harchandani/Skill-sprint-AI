from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.roadmap import RoadmapCreate, RoadmapResponse, RoadmapSummary, ShareResponse
from app.schemas.progress import RoadmapProgressResponse
from app.crud import roadmap as roadmap_crud
from app.crud import progress as progress_crud
from app.services.pdf_service import generate_roadmap_pdf

router = APIRouter(prefix="/roadmaps", tags=["roadmaps"])

@router.post("/create", response_model=RoadmapResponse)
def create_roadmap(
    roadmap: RoadmapCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new roadmap with sample week plans"""
    db_roadmap = roadmap_crud.create_roadmap(db, roadmap, current_user.id)
    return db_roadmap

@router.get("/{roadmap_id}", response_model=RoadmapResponse)
def get_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a roadmap by ID"""
    db_roadmap = roadmap_crud.get_roadmap(db, roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    # Verify ownership
    if db_roadmap.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this roadmap")
    
    return db_roadmap

@router.get("/{roadmap_id}/progress", response_model=RoadmapProgressResponse)
def get_roadmap_progress(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get progress statistics for a roadmap"""
    db_roadmap = roadmap_crud.get_roadmap(db, roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    # Verify ownership
    if db_roadmap.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this roadmap")
    
    try:
        progress = progress_crud.get_roadmap_progress(db, roadmap_id)
        return progress
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{roadmap_id}/export/pdf")
def export_roadmap_pdf(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export roadmap as PDF"""
    db_roadmap = roadmap_crud.get_roadmap(db, roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    # Verify ownership
    if db_roadmap.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this roadmap")
    
    try:
        progress_data = progress_crud.get_roadmap_progress(db, roadmap_id)
    except:
        progress_data = None
    
    pdf_buffer = generate_roadmap_pdf(db_roadmap, progress_data)
    filename = f"roadmap_{roadmap_id}_{db_roadmap.goal[:30].replace(' ', '_')}.pdf"
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post("/{roadmap_id}/share", response_model=ShareResponse)
def generate_share_link(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a public share link for a roadmap"""
    db_roadmap = roadmap_crud.get_roadmap(db, roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    # Verify ownership
    if db_roadmap.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this roadmap")
    
    if not db_roadmap.public_id:
        db_roadmap.generate_public_id()
        db.commit()
        db.refresh(db_roadmap)
    
    return ShareResponse(
        roadmap_id=roadmap_id,
        public_id=db_roadmap.public_id,
        share_url=f"/share/{db_roadmap.public_id}"
    )

@router.get("/", response_model=list[RoadmapSummary])
def get_all_roadmaps(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all roadmaps for current user with progress"""
    roadmaps = roadmap_crud.get_user_roadmaps(db, current_user.id, skip=skip, limit=limit)
    
    roadmap_summaries = []
    for roadmap in roadmaps:
        try:
            progress = progress_crud.get_roadmap_progress(db, roadmap.id)
            summary = RoadmapSummary(
                id=roadmap.id,
                goal=roadmap.goal,
                duration_weeks=roadmap.duration_weeks,
                created_at=roadmap.created_at,
                progress_percent=progress.progress_percent
            )
            roadmap_summaries.append(summary)
        except:
            summary = RoadmapSummary(
                id=roadmap.id,
                goal=roadmap.goal,
                duration_weeks=roadmap.duration_weeks,
                created_at=roadmap.created_at,
                progress_percent=0.0
            )
            roadmap_summaries.append(summary)
    
    return roadmap_summaries

@router.delete("/{roadmap_id}")
def delete_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a roadmap"""
    db_roadmap = roadmap_crud.get_roadmap(db, roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    # Verify ownership
    if db_roadmap.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this roadmap")
    
    db.delete(db_roadmap)
    db.commit()
    
    return {"message": "Roadmap deleted successfully"}

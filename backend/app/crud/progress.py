from sqlalchemy.orm import Session
from app.models.weekplan import WeekPlan
from app.models.progress import Progress
from app.models.roadmap import Roadmap
from app.schemas.progress import WeekCompleteResponse, WeekStatusResponse, RoadmapProgressResponse

def toggle_week_completion(db: Session, week_id: int) -> WeekCompleteResponse:
    """Toggle completion status for a week"""
    # Check if week exists
    week = db.query(WeekPlan).filter(WeekPlan.id == week_id).first()
    if not week:
        raise ValueError(f"Week with id {week_id} not found")
    
    # Check if progress record exists
    progress = db.query(Progress).filter(Progress.weekplan_id == week_id).first()
    
    if progress:
        # Toggle existing progress
        progress.completed = not progress.completed
        db.commit()
        db.refresh(progress)
        return WeekCompleteResponse(week_id=week_id, completed=progress.completed)
    else:
        # Create new progress record (mark as completed)
        new_progress = Progress(weekplan_id=week_id, completed=True)
        db.add(new_progress)
        db.commit()
        db.refresh(new_progress)
        return WeekCompleteResponse(week_id=week_id, completed=True)

def get_week_status(db: Session, week_id: int) -> WeekStatusResponse:
    """Get completion status for a specific week"""
    week = db.query(WeekPlan).filter(WeekPlan.id == week_id).first()
    if not week:
        raise ValueError(f"Week with id {week_id} not found")
    
    progress = db.query(Progress).filter(Progress.weekplan_id == week_id).first()
    completed = progress.completed if progress else False
    
    return WeekStatusResponse(week_id=week_id, completed=completed)

def get_roadmap_progress(db: Session, roadmap_id: int) -> RoadmapProgressResponse:
    """Get progress statistics for a roadmap"""
    # Check if roadmap exists
    roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    if not roadmap:
        raise ValueError(f"Roadmap with id {roadmap_id} not found")
    
    # Get all weeks for this roadmap
    weeks = db.query(WeekPlan).filter(WeekPlan.roadmap_id == roadmap_id).all()
    total_weeks = len(weeks)
    
    if total_weeks == 0:
        return RoadmapProgressResponse(
            roadmap_id=roadmap_id,
            completed_weeks=0,
            total_weeks=0,
            progress_percent=0.0
        )
    
    # Count completed weeks
    completed_weeks = 0
    for week in weeks:
        progress = db.query(Progress).filter(Progress.weekplan_id == week.id).first()
        if progress and progress.completed:
            completed_weeks += 1
    
    # Calculate percentage
    progress_percent = round((completed_weeks / total_weeks) * 100, 2)
    
    return RoadmapProgressResponse(
        roadmap_id=roadmap_id,
        completed_weeks=completed_weeks,
        total_weeks=total_weeks,
        progress_percent=progress_percent
    )

from sqlalchemy.orm import Session
from app.models.roadmap import Roadmap
from app.models.weekplan import WeekPlan
from app.schemas.roadmap import RoadmapCreate
from app.schemas.ai import GeneratedRoadmap

def create_roadmap(db: Session, roadmap_data: RoadmapCreate, user_id: int):
    """Create a new roadmap with sample week plans"""
    db_roadmap = Roadmap(
        goal=roadmap_data.goal,
        duration_weeks=roadmap_data.duration_weeks,
        user_id=user_id
    )
    db.add(db_roadmap)
    db.flush()

    for week in range(1, roadmap_data.duration_weeks + 1):
        week_plan = WeekPlan(
            roadmap_id=db_roadmap.id,
            week_number=week,
            focus_title=f"Week {week}: Sample Focus",
            topics_json=[f"Topic {week}.1", f"Topic {week}.2", f"Topic {week}.3"],
            tasks_json=[f"Task {week}.1", f"Task {week}.2"],
            target_problems=5
        )
        db.add(week_plan)

    db.commit()
    db.refresh(db_roadmap)
    return db_roadmap

def create_roadmap_from_ai(db: Session, goal: str, generated: GeneratedRoadmap, user_id: int, domain: str = None):
    """Create a roadmap from AI-generated data"""
    db_roadmap = Roadmap(
        goal=goal,
        duration_weeks=generated.duration_weeks,
        user_id=user_id,
        domain=domain
    )
    db.add(db_roadmap)
    db.flush()

    for week_data in generated.weeks:
        week_plan = WeekPlan(
            roadmap_id=db_roadmap.id,
            week_number=week_data.week,
            focus_title=week_data.focus,
            topics_json=week_data.topics,
            tasks_json=week_data.practice_tasks,
            target_problems=week_data.target_problems
        )
        db.add(week_plan)

    db.commit()
    db.refresh(db_roadmap)
    return db_roadmap

def get_roadmap(db: Session, roadmap_id: int):
    """Get roadmap by ID with all week plans"""
    return db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()

def get_user_roadmaps(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get all roadmaps for a specific user"""
    return db.query(Roadmap).filter(Roadmap.user_id == user_id).offset(skip).limit(limit).all()

def get_all_roadmaps(db: Session, skip: int = 0, limit: int = 100):
    """Get all roadmaps (admin only)"""
    return db.query(Roadmap).offset(skip).limit(limit).all()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text, or_, func
from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.weekplan import WeekPlan
from app.models.practice_item import PracticeItem
from app.models.domain_expansion import DomainExpansion
from app.schemas.practice import RecommendationResponse, PracticeItemResponse
from app.services.embedding_service import generate_embedding
from app.services.domain_detector import get_domain_from_roadmap_goal
from app.services.practice_library_expander import (
    expand_domain_library, 
    should_expand_domain,
    expand_topic_library,
    should_expand_topic
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/{week_id}", response_model=RecommendationResponse)
def get_recommendations(
    week_id: int,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get practice recommendations for a specific week using vector similarity search"""
    
    # Get the week plan (eagerly load roadmap)
    week = db.query(WeekPlan).options(joinedload(WeekPlan.roadmap)).filter(WeekPlan.id == week_id).first()
    if not week:
        raise HTTPException(status_code=404, detail="Week not found")
    
    # Access roadmap to ensure it's loaded
    roadmap = week.roadmap
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    # Verify ownership
    if roadmap.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this week")
    
    # Use stored domain or fallback to detection for old roadmaps
    domain = week.roadmap.domain
    if not domain:
        logger.info(f"No stored domain, detecting from goal: {week.roadmap.goal}")
        domain = get_domain_from_roadmap_goal(week.roadmap.goal)
    logger.info(f"Using domain: {domain} for week focus: {week.focus_title}")
    
    # Check if topic needs expansion (more specific than domain)
    if should_expand_topic(db, domain, week.focus_title, week.topics_json, min_items=3):
        logger.info(f"Topic '{week.focus_title}' in domain '{domain}' needs expansion")
        
        try:
            logger.info(f"Starting topic-specific expansion for: {week.focus_title}")
            
            # Generate topic-specific practice items
            generated_items = expand_topic_library(
                domain=domain,
                week_focus=week.focus_title,
                week_topics=week.topics_json,
                count=12
            )
            
            # Save to database
            items_added = 0
            for item_data in generated_items:
                practice_item = PracticeItem(
                    title=item_data['title'],
                    domain=item_data['domain'],
                    topic=item_data['topic'],
                    difficulty=item_data['difficulty'],
                    link=item_data['link'],
                    description=item_data['description'],
                    tags=item_data.get('tags', []),
                    embedding=item_data['embedding']
                )
                db.add(practice_item)
                items_added += 1
            
            db.commit()
            logger.info(f"✅ Expanded practice library for topic '{week.focus_title}' with {items_added} items")
            
        except Exception as e:
            logger.error(f"❌ Failed to expand topic '{week.focus_title}': {e}")
            db.rollback()
            # Continue with existing items if any
    
    # Check if domain needs expansion (fallback for general domain items)
    elif should_expand_domain(db, domain, min_items=5):
        logger.info(f"Domain '{domain}' needs expansion")
        
        # Check if already expanding or expanded
        expansion_record = db.query(DomainExpansion).filter(
            DomainExpansion.domain == domain
        ).first()
        
        if expansion_record and expansion_record.is_expanding:
            # Another request is already expanding this domain
            logger.info(f"Domain '{domain}' is already being expanded by another request")
        elif not expansion_record:
            # First time expanding this domain
            try:
                # Create expansion record with lock
                expansion_record = DomainExpansion(
                    domain=domain,
                    is_expanding=True
                )
                db.add(expansion_record)
                db.commit()
                
                logger.info(f"Starting dynamic expansion for domain: {domain}")
                
                # Generate practice items
                generated_items = expand_domain_library(
                    domain=domain,
                    topics=week.topics_json,
                    count=15
                )
                
                # Save to database
                items_added = 0
                for item_data in generated_items:
                    practice_item = PracticeItem(
                        title=item_data['title'],
                        domain=item_data['domain'],
                        topic=item_data['topic'],
                        difficulty=item_data['difficulty'],
                        link=item_data['link'],
                        description=item_data['description'],
                        tags=item_data.get('tags', []),
                        embedding=item_data['embedding']
                    )
                    db.add(practice_item)
                    items_added += 1
                
                # Update expansion record
                expansion_record.items_generated = items_added
                expansion_record.is_expanding = False
                db.commit()
                
                logger.info(f"✅ Expanded practice library for domain '{domain}' with {items_added} items")
                
            except Exception as e:
                logger.error(f"❌ Failed to expand domain '{domain}': {e}")
                # Release lock on error
                if expansion_record:
                    expansion_record.is_expanding = False
                    db.commit()
                # Continue with existing items if any
    
    # Create query text from week focus and topics
    query_text = f"{week.focus_title}. Topics: {', '.join(week.topics_json)}"
    
    try:
        # Generate embedding for the query
        query_embedding = generate_embedding(query_text)
        
        # Create search terms for tag matching
        search_terms = [week.focus_title.lower()] + [t.lower() for t in week.topics_json]
        
        # Perform topic-aware vector similarity search
        # Priority: items with matching tags/topics, then by similarity
        query = text("""
            WITH scored_items AS (
                SELECT 
                    id, title, domain, topic, difficulty, link, description, tags,
                    1 - (embedding <=> :query_embedding) as similarity,
                    CASE 
                        WHEN LOWER(topic) = ANY(:search_terms) THEN 3
                        WHEN EXISTS (
                            SELECT 1 FROM jsonb_array_elements_text(tags) AS tag
                            WHERE LOWER(tag) = ANY(:search_terms)
                        ) THEN 2
                        ELSE 1
                    END as relevance_boost
                FROM practice_items
                WHERE embedding IS NOT NULL
                  AND domain = :domain
            )
            SELECT id, title, domain, topic, difficulty, link, description, tags, similarity
            FROM scored_items
            ORDER BY relevance_boost DESC, similarity DESC
            LIMIT :limit
        """)
        
        result = db.execute(
            query,
            {
                "query_embedding": str(query_embedding),
                "domain": domain,
                "search_terms": search_terms,
                "limit": limit
            }
        )
        
        # Convert results to PracticeItemResponse
        recommendations = []
        for row in result:
            recommendations.append(PracticeItemResponse(
                id=row.id,
                title=row.title,
                domain=row.domain,
                topic=row.topic,
                difficulty=row.difficulty,
                link=row.link,
                description=row.description,
                tags=row.tags or []
            ))
        
        logger.info(f"Found {len(recommendations)} recommendations for domain '{domain}'")
        
        return RecommendationResponse(
            week_id=week_id,
            focus=week.focus_title,
            topics=week.topics_json,
            domain=domain,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Failed to generate recommendations: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )

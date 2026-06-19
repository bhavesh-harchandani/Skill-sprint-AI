"""
Dynamic Practice Library Expander
Automatically generates practice items for new domains using OpenAI
"""
import json
from typing import List, Dict
from openai import OpenAI
from app.core.config import settings
from app.services.embedding_service import generate_embedding
import logging

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def expand_domain_library(domain: str, topics: List[str], count: int = 15) -> List[Dict]:
    """
    Generate new practice items for a domain using OpenAI
    
    Args:
        domain: The learning domain (e.g., "Blockchain", "German", "Product Management")
        topics: List of topics from the week plan to guide generation
        count: Number of items to generate (default: 15)
    
    Returns:
        List of practice item dictionaries ready for database insertion
    """
    logger.info(f"Expanding practice library for domain: {domain} with {count} items")
    
    # Create prompt for OpenAI
    topics_str = ", ".join(topics) if topics else "general topics"
    
    prompt = f"""You are an expert learning coach creating practice exercises and resources.

Generate {count} high-quality practice items for learning {domain}.
Focus on topics like: {topics_str}

Requirements:
1. Mix of difficulties: 40% easy, 40% medium, 20% hard
2. Include variety: tutorials, projects, exercises, resources
3. Use REAL, TRUSTED links only:
   - Official documentation
   - Well-known learning platforms (Coursera, Udemy, freeCodeCamp, etc.)
   - GitHub repositories
   - YouTube tutorials from verified channels
   - If unsure, use the official docs or leave as generic placeholder
4. Make descriptions actionable and specific
5. Add 2-4 relevant tags per item

Output MUST be valid JSON array ONLY (no markdown, no explanation):
[
  {{
    "title": "Clear, specific title",
    "topic": "Specific topic within {domain}",
    "difficulty": "easy|medium|hard",
    "link": "https://real-url-or-official-docs",
    "description": "Actionable description of what to learn/build",
    "tags": ["tag1", "tag2", "tag3"]
  }}
]

Generate {count} items now:"""

    try:
        # Call OpenAI to generate practice items
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a learning resource curator. Output only valid JSON arrays."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        # Parse JSON
        generated_items = json.loads(content)
        
        if not isinstance(generated_items, list):
            raise ValueError("Generated content is not a JSON array")
        
        logger.info(f"Successfully generated {len(generated_items)} items for {domain}")
        
        # Add domain to each item and generate embeddings
        enriched_items = []
        for idx, item in enumerate(generated_items, 1):
            logger.info(f"  Processing item {idx}/{len(generated_items)}: {item.get('title', 'Unknown')}")
            
            # Validate required fields
            required_fields = ['title', 'topic', 'difficulty', 'link', 'description']
            if not all(field in item for field in required_fields):
                logger.warning(f"  Skipping item {idx}: Missing required fields")
                continue
            
            # Add domain
            item['domain'] = domain
            
            # Ensure tags exist
            if 'tags' not in item or not isinstance(item['tags'], list):
                item['tags'] = []
            
            # Generate embedding
            embedding_text = f"{domain} - {item['topic']}: {item['title']}. {item['description']}"
            try:
                item['embedding'] = generate_embedding(embedding_text)
                enriched_items.append(item)
                logger.info(f"  ✓ Generated embedding for: {item['title']}")
            except Exception as e:
                logger.error(f"  ✗ Failed to generate embedding for item {idx}: {e}")
                continue
        
        logger.info(f"Successfully enriched {len(enriched_items)} items with embeddings")
        return enriched_items
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from OpenAI response: {e}")
        logger.error(f"Response content: {content[:500]}")
        raise ValueError(f"Invalid JSON response from OpenAI: {e}")
    except Exception as e:
        logger.error(f"Error expanding domain library: {e}")
        raise


def should_expand_domain(db, domain: str, min_items: int = 5) -> bool:
    """
    Check if a domain needs expansion
    
    Args:
        db: Database session
        domain: Domain to check
        min_items: Minimum number of items required
    
    Returns:
        True if domain needs expansion, False otherwise
    """
    from app.models.practice_item import PracticeItem
    
    count = db.query(PracticeItem).filter(PracticeItem.domain == domain).count()
    logger.info(f"Domain '{domain}' has {count} items (minimum: {min_items})")
    
    return count < min_items


def should_expand_topic(db, domain: str, week_focus: str, week_topics: List[str], min_items: int = 3) -> bool:
    """
    Check if a specific topic within a domain needs expansion
    
    Args:
        db: Database session
        domain: Domain to check
        week_focus: Week focus title
        week_topics: List of week topics
        min_items: Minimum number of items required for this topic
    
    Returns:
        True if topic needs expansion, False otherwise
    """
    from app.models.practice_item import PracticeItem
    from sqlalchemy import or_, func
    
    # Create search terms from focus and topics
    search_terms = [week_focus.lower()] + [t.lower() for t in week_topics]
    
    # Count items that match domain and have any of the search terms in tags or topic
    count = 0
    for term in search_terms:
        term_count = db.query(PracticeItem).filter(
            PracticeItem.domain == domain,
            or_(
                func.lower(PracticeItem.topic).contains(term),
                PracticeItem.tags.contains([term])
            )
        ).count()
        count = max(count, term_count)
    
    logger.info(f"Topic '{week_focus}' in domain '{domain}' has {count} matching items (minimum: {min_items})")
    
    return count < min_items


def expand_topic_library(domain: str, week_focus: str, week_topics: List[str], count: int = 12) -> List[Dict]:
    """
    Generate new practice items for a specific topic within a domain
    
    Args:
        domain: The learning domain
        week_focus: The specific focus for this week
        week_topics: List of topics from the week plan
        count: Number of items to generate (default: 12)
    
    Returns:
        List of practice item dictionaries ready for database insertion
    """
    logger.info(f"Expanding topic library for '{week_focus}' in domain '{domain}' with {count} items")
    
    # Create focused prompt
    topics_str = ", ".join(week_topics) if week_topics else week_focus
    
    prompt = f"""You are an expert learning coach creating practice exercises and resources.

Generate {count} high-quality practice items specifically for: {week_focus}
Domain: {domain}
Related topics: {topics_str}

Requirements:
1. ALL items MUST be directly related to "{week_focus}"
2. Mix of difficulties: 40% easy, 40% medium, 20% hard
3. Include variety: tutorials, projects, exercises, resources
4. Use REAL, TRUSTED links only:
   - Official documentation
   - Well-known learning platforms (Coursera, Udemy, freeCodeCamp, LeetCode, HackerRank, etc.)
   - GitHub repositories
   - YouTube tutorials from verified channels
   - If unsure, use the official docs or leave as generic placeholder
5. Make descriptions actionable and specific to "{week_focus}"
6. Add 2-4 relevant tags per item, MUST include "{week_focus.lower()}" as a tag

Output MUST be valid JSON array ONLY (no markdown, no explanation):
[
  {{
    "title": "Clear, specific title related to {week_focus}",
    "topic": "{week_focus}",
    "difficulty": "easy|medium|hard",
    "link": "https://real-url-or-official-docs",
    "description": "Actionable description specific to {week_focus}",
    "tags": ["{week_focus.lower()}", "tag2", "tag3"]
  }}
]

Generate {count} items now:"""

    try:
        # Call OpenAI to generate practice items
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a learning resource curator. Output only valid JSON arrays."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        # Parse JSON
        generated_items = json.loads(content)
        
        if not isinstance(generated_items, list):
            raise ValueError("Generated content is not a JSON array")
        
        logger.info(f"Successfully generated {len(generated_items)} items for topic '{week_focus}'")
        
        # Add domain to each item and generate embeddings
        enriched_items = []
        for idx, item in enumerate(generated_items, 1):
            logger.info(f"  Processing item {idx}/{len(generated_items)}: {item.get('title', 'Unknown')}")
            
            # Validate required fields
            required_fields = ['title', 'topic', 'difficulty', 'link', 'description']
            if not all(field in item for field in required_fields):
                logger.warning(f"  Skipping item {idx}: Missing required fields")
                continue
            
            # Add domain
            item['domain'] = domain
            
            # Ensure tags exist and include week_focus
            if 'tags' not in item or not isinstance(item['tags'], list):
                item['tags'] = []
            
            # Add week_focus to tags if not present
            focus_lower = week_focus.lower()
            if focus_lower not in [tag.lower() for tag in item['tags']]:
                item['tags'].insert(0, focus_lower)
            
            # Generate embedding
            embedding_text = f"{domain} - {item['topic']}: {item['title']}. {item['description']}"
            try:
                item['embedding'] = generate_embedding(embedding_text)
                enriched_items.append(item)
                logger.info(f"  ✓ Generated embedding for: {item['title']}")
            except Exception as e:
                logger.error(f"  ✗ Failed to generate embedding for item {idx}: {e}")
                continue
        
        logger.info(f"Successfully enriched {len(enriched_items)} topic-specific items with embeddings")
        return enriched_items
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from OpenAI response: {e}")
        logger.error(f"Response content: {content[:500]}")
        raise ValueError(f"Invalid JSON response from OpenAI: {e}")
    except Exception as e:
        logger.error(f"Error expanding topic library: {e}")
        raise

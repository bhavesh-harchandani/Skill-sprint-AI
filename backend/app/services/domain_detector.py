"""
AI-powered domain detection service
Automatically detects learning domain from roadmap goal using OpenAI
"""
from openai import OpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def detect_domain_with_ai(goal: str) -> str:
    """
    Detect the learning domain from a roadmap goal using OpenAI
    
    Args:
        goal: The learning goal (e.g., "I want to learn Blockchain")
    
    Returns:
        Domain name (1-3 words, e.g., "Blockchain", "Product Management")
    """
    logger.info(f"Detecting domain for goal: {goal}")
    
    prompt = f"""Classify this learning goal into a short domain label (1-3 words maximum).

Learning Goal: "{goal}"

Rules:
1. Return ONLY the domain name, no explanation
2. Use 1-3 words maximum
3. Be specific but concise
4. Use title case (e.g., "Machine Learning", "Web Development")
5. Common domains: DSA, React, DevOps, Machine Learning, Blockchain, Product Management, etc.

Domain:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a learning domain classifier. Output only the domain name, nothing else."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Low temperature for consistent classification
            max_tokens=10
        )
        
        domain = response.choices[0].message.content.strip()
        
        # Clean up the response
        domain = domain.replace('"', '').replace("'", '').strip()
        
        # Ensure it's not too long
        if len(domain.split()) > 3:
            # Take first 3 words
            domain = ' '.join(domain.split()[:3])
        
        logger.info(f"Detected domain: {domain}")
        return domain
        
    except Exception as e:
        logger.error(f"Error detecting domain with AI: {e}")
        # Fallback to "General" if AI fails
        return "General"


def get_domain_from_roadmap_goal(goal: str) -> str:
    """
    Extract domain from roadmap goal using AI
    This is the main function used throughout the app
    
    Args:
        goal: The learning goal
    
    Returns:
        Detected domain name
    """
    return detect_domain_with_ai(goal)

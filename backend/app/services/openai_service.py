from openai import AsyncOpenAI
from app.core.config import settings
from app.schemas.ai import GeneratedRoadmap
import json

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_roadmap(goal: str, answers: dict, duration_weeks: int) -> GeneratedRoadmap:
    """
    Generate a personalized learning roadmap using GPT-4o-mini.
    Returns structured roadmap with week-by-week breakdown.
    """
    
    # Format answers for the prompt
    answers_text = "\n".join([f"- {k}: {v}" for k, v in answers.items()])
    
    system_prompt = """You are an expert learning mentor and curriculum designer. Your job is to create personalized, structured learning roadmaps.

Given a learning goal, user context, and duration, generate a detailed week-by-week learning roadmap.

Requirements:
1. Each week should have a clear focus area
2. Include 3-5 specific topics per week
3. Provide actionable practice tasks (2-4 per week)
4. Set realistic target problems/exercises per week
5. Progress from fundamentals to advanced topics
6. Adapt difficulty based on user's level
7. Consider time availability when setting targets

For different domains:
- DSA: Focus on data structures, algorithms, problem-solving patterns
- Machine Learning: Cover math foundations, libraries, projects
- DevOps: Include tools, cloud platforms, CI/CD, monitoring
- Web Development: Cover frontend/backend, frameworks, projects
- Other domains: Adapt accordingly

CRITICAL: Return ONLY valid JSON in this exact format:
{
  "title": "Descriptive roadmap title",
  "duration_weeks": <number>,
  "weeks": [
    {
      "week": 1,
      "focus": "Week focus title",
      "topics": ["topic1", "topic2", "topic3"],
      "practice_tasks": ["task1", "task2"],
      "target_problems": <number>
    }
  ]
}

No markdown, no explanations, just pure JSON."""

    user_prompt = f"""Learning Goal: {goal}

User Context:
{answers_text}

Duration: {duration_weeks} weeks

Generate a personalized {duration_weeks}-week learning roadmap as JSON."""

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2500,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON response
        parsed = json.loads(content)
        
        # Validate structure
        if not isinstance(parsed, dict):
            raise ValueError("Response is not a JSON object")
        
        # Ensure required fields exist
        if "weeks" not in parsed:
            raise ValueError("Missing 'weeks' field in response")
        
        if "title" not in parsed:
            parsed["title"] = f"{goal} - Learning Roadmap"
        
        if "duration_weeks" not in parsed:
            parsed["duration_weeks"] = duration_weeks
        
        # Validate weeks array
        if not isinstance(parsed["weeks"], list) or len(parsed["weeks"]) == 0:
            raise ValueError("Invalid or empty 'weeks' array")
        
        # Ensure we have the right number of weeks
        if len(parsed["weeks"]) != duration_weeks:
            # Adjust if needed
            if len(parsed["weeks"]) < duration_weeks:
                raise ValueError(f"Generated only {len(parsed['weeks'])} weeks, expected {duration_weeks}")
            else:
                parsed["weeks"] = parsed["weeks"][:duration_weeks]
        
        # Validate each week structure
        for i, week in enumerate(parsed["weeks"], 1):
            if not isinstance(week, dict):
                raise ValueError(f"Week {i} is not a valid object")
            
            # Ensure required fields
            if "week" not in week:
                week["week"] = i
            if "focus" not in week:
                raise ValueError(f"Week {i} missing 'focus' field")
            if "topics" not in week or not isinstance(week["topics"], list):
                raise ValueError(f"Week {i} missing or invalid 'topics' field")
            if "practice_tasks" not in week or not isinstance(week["practice_tasks"], list):
                raise ValueError(f"Week {i} missing or invalid 'practice_tasks' field")
            if "target_problems" not in week:
                week["target_problems"] = 5  # Default value
        
        # Create and validate Pydantic model
        roadmap = GeneratedRoadmap(**parsed)
        return roadmap
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Roadmap generation error: {str(e)}")

async def generate_clarifying_questions(goal: str) -> list[str]:
    """
    Generate up to 5 clarifying questions for a learning goal using GPT-4o-mini.
    Returns strict JSON array of questions.
    """
    
    system_prompt = """You are an expert learning mentor. Your job is to ask clarifying questions to understand the learner's context better.

Given a learning goal, generate 3-5 smart, relevant clarifying questions that will help create a personalized learning roadmap.

Questions should cover:
- Current skill level (beginner/intermediate/advanced)
- Time availability (hours per day, total weeks)
- Programming language preference (if applicable)
- Learning objective (interviews, projects, academics, career switch)
- Prior experience or background

Adapt questions based on the specific goal. For example:
- DSA: Ask about programming language, interview prep vs academics
- Machine Learning: Ask about math background, Python experience
- DevOps: Ask about current role, cloud platform preference
- Web Development: Ask about frontend/backend preference

CRITICAL: Return ONLY a valid JSON array of strings. No explanations, no markdown, no extra text.
Format: ["question1", "question2", "question3", "question4", "question5"]
Maximum 5 questions."""

    user_prompt = f"Learning goal: {goal}\n\nGenerate clarifying questions as a JSON array."

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON response
        parsed = json.loads(content)
        
        # Handle different possible JSON structures
        if isinstance(parsed, list):
            questions = parsed
        elif isinstance(parsed, dict):
            # Try common keys
            questions = parsed.get('questions', parsed.get('Questions', parsed.get('items', [])))
        else:
            raise ValueError("Unexpected JSON structure")
        
        # Validate and limit to 5 questions
        if not questions or not isinstance(questions, list):
            raise ValueError("No valid questions array found in response")
        
        questions = [str(q).strip() for q in questions if q][:5]
        
        if len(questions) < 3:
            raise ValueError("Insufficient questions generated")
        
        return questions
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

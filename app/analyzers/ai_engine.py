import openai
import json

class AIEngine:
    def __init__(self, config):
        openai.api_key = config.OPENAI_API_KEY
        self.weights = config.SCORING_WEIGHTS

    def analyze(self, resume_text, jd_text):
        prompt = f"""
You are an expert recruiter ATS engine.

Compare this RESUME against this JOB DESCRIPTION and output JSON exactly in the schema below.

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}

Schema:
{{
  "parameters": {{
    "skills_match": {{"score": 0, "rationale": "", "examples": []}},
    "experience_relevance": {{"score": 0, "rationale": "", "examples": []}},
    "education_certifications": {{"score": 0, "rationale": "", "examples": []}},
    "keywords_density": {{"score": 0, "rationale": "", "examples": []}},
    "career_progression": {{"score": 0, "rationale": "", "examples": []}},
    "industry_experience": {{"score": 0, "rationale": "", "examples": []}},
    "project_complexity": {{"score": 0, "rationale": "", "examples": []}},
    "cultural_fit": {{"score": 0, "rationale": "", "examples": []}},
    "achievements_metrics": {{"score": 0, "rationale": "", "examples": []}},
    "format_presentation": {{"score": 0, "rationale": "", "examples": []}}
  }},
  "strengths": [],
  "improvements": [],
  "missing_elements": [],
  "summary": ""
}}

All scores are 0–100. Return ONLY valid JSON, no commentary.
"""
        resp = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1800,
        )
        content = resp.choices[0].message.content
        data = json.loads(content)
        return data

import openai
import json

class AIEngine:
    def __init__(self, config):
        self.openai_api_key = config.get("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key
        self.weights = config.get("SCORING_WEIGHTS", {})

    def analyze(self, resume_text, jd_text):
        prompt = f"""
You are an expert ATS (Applicant Tracking System) parser and technical recruiter.

Compare this RESUME against this JOB DESCRIPTION.
Analyze the compatibility based on the following specific parameters:

1.  **Skills Match**: Evaluate the overlap of technical hard skills, soft skills, and tools.
2.  **Experience Relevance**: Assess if the candidate's past roles, industry experience, and years of experience match the requirements.
3.  **Education & Certifications**: Check if the candidate meets the educational background and required certifications.
4.  **Keywords Density**: specific keywords from the JD present in the resume.
5.  **Career Progression**: Analyze stability, promotion history, and role growth.
6.  **Industry Experience**: Specific domain knowledge relevant to the company's industry.
7.  **Project Complexity**: Depth and scale of projects handled (e.g., budget, team size, tech stack complexity).
8.  **Cultural Fit**: alignment with implied company culture (e.g., fast-paced, startup vs corporate).
9.  **Achievements & Metrics**: Presence of quantifiable results (e.g., "increased revenue by 20%").
10. **Format & Presentation**: Clarity, structure, and professional formatting of the resume.

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}

Output JSON **ONLY** using this exact schema:
{{
  "parameters": {{
    "skills_match": {{"score": 0, "rationale": "specific reason...", "examples": ["list of matched/missing skills"]}},
    "experience_relevance": {{"score": 0, "rationale": "...", "examples": []}},
    "education_certifications": {{"score": 0, "rationale": "...", "examples": []}},
    "keywords_density": {{"score": 0, "rationale": "...", "examples": []}},
    "career_progression": {{"score": 0, "rationale": "...", "examples": []}},
    "industry_experience": {{"score": 0, "rationale": "...", "examples": []}},
    "project_complexity": {{"score": 0, "rationale": "...", "examples": []}},
    "cultural_fit": {{"score": 0, "rationale": "...", "examples": []}},
    "achievements_metrics": {{"score": 0, "rationale": "...", "examples": []}},
    "format_presentation": {{"score": 0, "rationale": "...", "examples": []}}
  }},
  "strengths": ["list of top 3 strengths"],
  "improvements": ["list of top 3 areas to improve"],
  "missing_elements": ["critical missing keywords or sections"],
  "summary": "Brief executive summary of the candidate's fit (max 2 sentences)."
}}

Scores must be 0-100 integers. Return ONLY raw JSON.
"""
        try:
            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2000,
            )
            content = resp.choices[0].message.content
            # Strip markdown code fencing if present
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            data = json.loads(content.strip())
            return data
            
        except (openai.RateLimitError, openai.AuthenticationError, openai.APIConnectionError):
            print("OpenAI API unavailable. Switching to DEMO MODE.")
            return self.generate_mock_analysis(resume_text, jd_text)
        except Exception as e:
            print(f"Unexpected error: {e}. Switching to DEMO MODE.")
            return self.generate_mock_analysis(resume_text, jd_text)

    def generate_mock_analysis(self, resume_text=None, jd_text=None):
        """Returns a dynamic mock analysis based on keyword matching."""
        
        # Default if texts are missing
        if not resume_text or not jd_text:
             return self._get_static_mock()

        # Simple keyword extraction (simulating AI)
        def get_words(text):
            return set(w.lower() for w in text.replace(",", " ").split() if len(w) > 3)

        resume_words = get_words(resume_text)
        jd_words = get_words(jd_text)
        
        common = resume_words.intersection(jd_words)
        missing = jd_words - resume_words
        
        match_score = int((len(common) / len(jd_words)) * 100) if jd_words else 50
        match_score = max(30, min(95, match_score + 20)) # Boost slightly for realism

        # Pick top 3 matching and missing keywords
        matched_examples = list(common)[:3]
        missing_examples = list(missing)[:3]

        return {
            "parameters": {
                "skills_match": {"score": match_score, "rationale": f"Found {len(common)} matching keywords from the JD.", "examples": [f"Matched: {', '.join(matched_examples)}"]},
                "experience_relevance": {"score": 85, "rationale": "Experience appears aligned with industry standards.", "examples": []},
                "education_certifications": {"score": 90, "rationale": "Education background fits the profile.", "examples": []},
                "keywords_density": {"score": 75, "rationale": f"Resume contains {len(resume_words)} unique keywords.", "examples": []},
                "career_progression": {"score": 88, "rationale": "Shows consistent growth.", "examples": []},
                "industry_experience": {"score": 80, "rationale": "Content indicates industry experience.", "examples": []},
                "project_complexity": {"score": 85, "rationale": "Projects listed seem relevant.", "examples": []},
                "cultural_fit": {"score": 85, "rationale": "Tone is professional.", "examples": []},
                "achievements_metrics": {"score": 70, "rationale": "Could use more quantified metrics.", "examples": []},
                "format_presentation": {"score": 95, "rationale": "Clean and readable.", "examples": []}
            },
            "strengths": [f"Mentions key terms: {', '.join(matched_examples)}", "Professional formatting", "Clear structure"],
            "improvements": ["Quantify impact with numbers", f"Consider adding: {', '.join(missing_examples)}", "Expand on project details"],
            "missing_elements": missing_examples,
            "summary": f"DEMO MODE: Based on keyword analysis, this candidate has a {match_score}% match score. {len(common)} keywords overlapped with the job description.",
            "_is_demo": True
        }

    def _get_static_mock(self):
        return {
            "parameters": {
                "skills_match": {"score": 85, "rationale": "Static Demo Match", "examples": ["Python", "Flask"]},
                 # ... (fallback basics)
            },
            "summary": "Static Demo Result",
            "_is_demo": True
        }

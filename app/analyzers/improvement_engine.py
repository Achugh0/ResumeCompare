import openai
import json

class ImprovementEngine:
    """
    Generates actionable improvement suggestions based on analysis results.
    Provides specific examples and optionally creates an improved resume.
    """
    
    def __init__(self, config):
        self.openai_api_key = config.get("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key
    
    def generate_suggestions(self, analysis_data, resume_text, jd_text):
        """
        Generate specific, actionable improvement suggestions.
        
        Args:
            analysis_data: The scored analysis results
            resume_text: Original resume text
            jd_text: Job description text
            
        Returns:
            dict: Structured suggestions with examples
        """
        try:
            improvements = analysis_data.get("improvements", [])
            missing_elements = analysis_data.get("missing_elements", [])
            
            prompt = f"""
You are an expert resume writer and career coach.

Analyze this ACTUAL RESUME and provide SPECIFIC, TAILORED suggestions for improvement.

**CRITICAL INSTRUCTIONS**:
1. Read the ACTUAL resume content below carefully
2. For "Before" examples, extract REAL text from the candidate's resume (not generic examples)
3. For "After" examples, show how to improve THAT SPECIFIC content
4. If something is missing, suggest where/how to add it based on their existing experience
5. Reference actual job titles, companies, or achievements from their resume

**IMPROVEMENTS NEEDED**:
{chr(10).join(f"- {imp}" for imp in improvements)}

**MISSING ELEMENTS**:
{chr(10).join(f"- {elem}" for elem in missing_elements)}

**JOB DESCRIPTION**:
{jd_text[:1500]}

**CANDIDATE'S ACTUAL RESUME**:
{resume_text}

For each improvement area, provide:
1. **What to Add/Change**: Specific instruction tailored to THIS candidate
2. **Example Before**: Extract ACTUAL text from their resume (or state "Not currently present")
3. **Example After**: Show how to improve THAT SPECIFIC text, maintaining their voice
4. **Why It Helps**: Brief rationale (1 sentence)

**IMPORTANT**: 
- Use REAL content from the resume for "Before" examples
- Make "After" examples feel authentic to this candidate's experience
- Don't invent experiences they don't have
- Suggest realistic improvements based on what they've actually done

Output JSON ONLY with this structure:
{{
  "suggestions": [
    {{
      "area": "Improvement area name",
      "what_to_change": "Specific instruction for THIS candidate",
      "before": "Actual text from their resume or 'Not currently present'",
      "after": "Improved version of THEIR content",
      "rationale": "Why this helps"
    }}
  ],
  "_is_demo": false
}}

Provide 3-5 high-impact, RESUME-SPECIFIC suggestions.
"""
            
            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2500,
            )
            
            content = resp.choices[0].message.content
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            data = json.loads(content.strip())
            return data
            
        except openai.RateLimitError as e:
            print(f"[SUGGESTIONS] OpenAI Rate Limit Error: {e}")
            return self._generate_mock_suggestions(analysis_data, resume_text, jd_text)
        except openai.AuthenticationError as e:
            print(f"[SUGGESTIONS] OpenAI Authentication Error: {e}")
            return self._generate_mock_suggestions(analysis_data, resume_text, jd_text)
        except openai.APIConnectionError as e:
            print(f"[SUGGESTIONS] OpenAI Connection Error: {e}")
            return self._generate_mock_suggestions(analysis_data, resume_text, jd_text)
        except json.JSONDecodeError as e:
            print(f"[SUGGESTIONS] JSON Decode Error: {e}. Response was: {content if 'content' in locals() else 'N/A'}")
            return self._generate_mock_suggestions(analysis_data, resume_text, jd_text)
        except Exception as e:
            print(f"[SUGGESTIONS] Unexpected Error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return self._generate_mock_suggestions(analysis_data, resume_text, jd_text)
    
    def _generate_mock_suggestions(self, analysis_data, resume_text, jd_text):
        """
        Generate tailored mock suggestions by extracting real content from the resume.
        Ensures the tool "listens" even when the API is offline (Quota 429).
        """
        import re
        
        # Extract potential bullet points or short sentences from the resume
        sentences = re.split(r'[•\n\r|;]', resume_text)
        real_bullets = [s.strip() for s in sentences if len(s.strip()) > 30 and len(s.strip()) < 150]
        
        # Fallback if no good bullets found
        if not real_bullets:
            real_bullets = ["Managed key projects and improved team delivery", "Responsible for core system components"]
            
        improvements = analysis_data.get("improvements", [])
        missing_elements = analysis_data.get("missing_elements", [])
        
        suggestions = []
        
        # Suggestion 1: Quantify Impact (Using a real bullet if possible)
        bullet_to_improve = real_bullets[0] if len(real_bullets) > 0 else "Managed a team and improved processes"
        suggestions.append({
            "area": "Quantify Your Impact",
            "what_to_change": "Add specific metrics, percentages, or numbers to this achievement to demonstrate scale.",
            "before": bullet_to_improve,
            "after": f"{bullet_to_improve} (e.g., 'resulting in 25% efficiency gain and $50k cost savings')",
            "rationale": "Quantified achievements provide concrete evidence of your capabilities and make your contributions more memorable."
        })
        
        # Suggestion 2: Add Missing Skills
        if missing_elements:
            missing_sample = missing_elements[:3]
            suggestions.append({
                "area": "Incorporate Missing Keywords",
                "what_to_change": f"Add relevant experience or skills related to: {', '.join(missing_sample)}",
                "before": "Not clearly highlighted in current resume",
                "after": f"Leveraged {missing_sample[0]} and {missing_sample[1] if len(missing_sample) > 1 else 'relevant tools'} to deliver project goals...",
                "rationale": "Including job-specific keywords improves ATS compatibility and shows direct alignment with the role."
            })
        
        # Suggestion 3: Strengthen Action Verbs (Using another real bullet)
        bullet_2 = real_bullets[min(1, len(real_bullets)-1)] if len(real_bullets) > 1 else "Worked on various software features"
        suggestions.append({
            "area": "Use Stronger Action Verbs",
            "what_to_change": "Replace passive language with powerful action verbs that demonstrate leadership.",
            "before": bullet_2,
            "after": f"Accelerated / Spearheaded {bullet_2.lower() if bullet_2[0].islower() else bullet_2}",
            "rationale": "Strong action verbs create a more dynamic narrative and position you as a proactive contributor."
        })
        
        # Suggestion 4: Highlight Key Experience
        if len(real_bullets) > 2:
            bullet_3 = real_bullets[2]
            suggestions.append({
                "area": "Expand on Core Achievements",
                "what_to_change": "Provide more context about the scale and complexity of this specific task.",
                "before": bullet_3,
                "after": f"{bullet_3} for a [Team Size/Scale] project, managing [specific tool/process]...",
                "rationale": "Context helps recruiters understand the magnitude of your responsibilities."
            })
        
        return {
            "suggestions": suggestions[:4],
            "_is_demo": True,
            "_demo_reason": "API Quota Exceeded (429)" 
        }
    
    def create_improved_resume_text(self, resume_text, suggestions_data):
        """
        Create an improved version of the resume incorporating suggestions.
        Returns improved text that can be downloaded.
        
        Args:
            resume_text: Original resume text
            suggestions_data: Suggestions from generate_suggestions()
            
        Returns:
            str: Improved resume text with suggestions incorporated
        """
        suggestions = suggestions_data.get("suggestions", [])
        
        # For now, return a formatted improvement guide
        # In a full implementation, this would use python-docx to create a .docx file
        
        improved_text = f"""
IMPROVED RESUME SUGGESTIONS
============================

Based on the analysis, here are specific improvements to make:

"""
        
        for i, suggestion in enumerate(suggestions, 1):
            improved_text += f"""
{i}. {suggestion['area']}
   
   What to Change: {suggestion['what_to_change']}
   
   Before: {suggestion['before']}
   
   After: {suggestion['after']}
   
   Why: {suggestion['rationale']}

---

"""
        
        improved_text += """

NEXT STEPS:
1. Review each suggestion above
2. Update your resume with the "After" examples
3. Ensure all changes maintain your authentic voice
4. Re-run the analysis to see your improved score!
"""
        
        return improved_text

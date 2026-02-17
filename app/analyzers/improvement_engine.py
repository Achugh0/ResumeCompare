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
        Generate realistic mock suggestions when API is unavailable.
        """
        improvements = analysis_data.get("improvements", [])
        missing_elements = analysis_data.get("missing_elements", [])
        
        suggestions = []
        
        # Suggestion 1: Quantify Impact
        if any("quantif" in imp.lower() or "metric" in imp.lower() for imp in improvements):
            suggestions.append({
                "area": "Quantify Your Impact",
                "what_to_change": "Add specific metrics, percentages, or numbers to demonstrate the scale and impact of your work.",
                "before": "Managed a team and improved processes",
                "after": "Led a cross-functional team of 8 engineers, reducing deployment time by 40% and improving system uptime to 99.9%",
                "rationale": "Quantified achievements provide concrete evidence of your capabilities and make your contributions more memorable."
            })
        
        # Suggestion 2: Add Missing Skills
        if missing_elements:
            missing_sample = missing_elements[:3]
            suggestions.append({
                "area": "Incorporate Missing Keywords",
                "what_to_change": f"Add relevant experience or skills related to: {', '.join(missing_sample)}",
                "before": "Not present in current resume",
                "after": f"Utilized {missing_sample[0]} to optimize workflows, collaborating with teams on {missing_sample[1] if len(missing_sample) > 1 else 'key initiatives'}",
                "rationale": "Including job-specific keywords improves ATS compatibility and shows direct alignment with the role requirements."
            })
        
        # Suggestion 3: Strengthen Action Verbs
        suggestions.append({
            "area": "Use Stronger Action Verbs",
            "what_to_change": "Replace passive or weak verbs with powerful action verbs that demonstrate leadership and initiative.",
            "before": "Was responsible for handling customer issues",
            "after": "Resolved 200+ customer escalations monthly, achieving a 95% satisfaction rating and reducing churn by 15%",
            "rationale": "Strong action verbs create a more dynamic narrative and position you as a proactive contributor."
        })
        
        # Suggestion 4: Add Context and Scope
        suggestions.append({
            "area": "Provide Context and Scope",
            "what_to_change": "Include details about team size, budget, project scale, or organizational impact.",
            "before": "Developed new features for the platform",
            "after": "Architected and delivered 5 core features for a SaaS platform serving 50,000+ users, managing a $200K budget",
            "rationale": "Context helps recruiters understand the magnitude of your responsibilities and the complexity of your work."
        })
        
        # Suggestion 5: Highlight Relevant Certifications/Projects
        if any("qualif" in imp.lower() or "cert" in imp.lower() for imp in improvements):
            suggestions.append({
                "area": "Add Relevant Certifications or Projects",
                "what_to_change": "Include certifications, courses, or side projects that demonstrate continuous learning and relevant expertise.",
                "before": "Not present in current resume",
                "after": "Certifications: AWS Solutions Architect (2024), Kubernetes Administrator (CKA) | Open Source: Contributor to [relevant project]",
                "rationale": "Certifications and projects validate your skills and show commitment to professional development."
            })
        
        return {
            "suggestions": suggestions[:5],  # Return top 5
            "_is_demo": True
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

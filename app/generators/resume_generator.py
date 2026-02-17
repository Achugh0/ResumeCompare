import openai
import json
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
from datetime import datetime

class ATSResumeGenerator:
    """
    Generates ATS-friendly resumes in Word and PDF formats.
    Applies improvement suggestions to create an enhanced resume.
    """
    
    def __init__(self, config):
        self.openai_api_key = config.get("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key
    
    def generate_improved_resume(self, resume_text, suggestions_data, analysis_data, jd_text):
        """
        Generate an improved resume by applying suggestions.
        
        Args:
            resume_text: Original resume text
            suggestions_data: Suggestions from ImprovementEngine
            analysis_data: Analysis results
            jd_text: Job description text
            
        Returns:
            dict: Structured resume content
        """
        try:
            suggestions = suggestions_data.get("suggestions", [])
            
            # Build suggestions summary for AI
            suggestions_text = "\n".join([
                f"{i+1}. {s['area']}: {s['what_to_change']}\n   Before: {s['before']}\n   After: {s['after']}"
                for i, s in enumerate(suggestions)
            ])
            
            prompt = f"""
You are an expert resume writer specializing in ATS-optimized resumes.

**TASK**: Transform this resume by applying the improvement suggestions while maintaining an ATS-friendly format.

**ORIGINAL RESUME**:
{resume_text}

**JOB DESCRIPTION** (for context):
{jd_text[:1500]}

**IMPROVEMENT SUGGESTIONS TO APPLY**:
{suggestions_text}

**INSTRUCTIONS**:
1. Parse the original resume structure
2. Apply each suggestion to the appropriate section
3. Enhance content while maintaining the candidate's authentic voice
4. Format in clean ATS-friendly structure
5. Include relevant keywords from the job description
6. Quantify achievements where possible

**OUTPUT FORMAT** (JSON):
{{
  "contact": {{
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "+1234567890",
    "location": "City, State",
    "linkedin": "linkedin.com/in/profile" (optional)
  }},
  "summary": "2-3 sentence professional summary highlighting key value proposition",
  "experience": [
    {{
      "title": "Job Title",
      "company": "Company Name",
      "location": "City, State",
      "dates": "MMM YYYY - MMM YYYY",
      "achievements": [
        "Achievement with metrics and impact",
        "Another achievement with specific results"
      ]
    }}
  ],
  "skills": {{
    "Technical": ["skill1", "skill2"],
    "Tools": ["tool1", "tool2"],
    "Other": ["skill1", "skill2"]
  }},
  "education": [
    {{
      "degree": "Degree Name",
      "institution": "University Name",
      "year": "YYYY",
      "details": "GPA, honors, etc." (optional)
    }}
  ],
  "certifications": [
    "Certification Name (Year)",
    "Another Certification (Year)"
  ]
}}

**CRITICAL**:
- Use REAL information from the original resume
- Apply the suggestions to improve content
- Don't invent experiences or credentials
- Keep it ATS-friendly (no tables, graphics, or complex formatting)
- Output ONLY valid JSON
"""
            
            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=3000,
            )
            
            content = resp.choices[0].message.content
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            resume_data = json.loads(content.strip())
            resume_data["_is_demo"] = False
            return resume_data
            
        except openai.RateLimitError as e:
            print(f"[RESUME GEN] OpenAI Rate Limit Error: {e}")
            return self._generate_template_resume(resume_text, suggestions_data)
        except openai.AuthenticationError as e:
            print(f"[RESUME GEN] OpenAI Authentication Error: {e}")
            return self._generate_template_resume(resume_text, suggestions_data)
        except openai.APIConnectionError as e:
            print(f"[RESUME GEN] OpenAI Connection Error: {e}")
            return self._generate_template_resume(resume_text, suggestions_data)
        except json.JSONDecodeError as e:
            print(f"[RESUME GEN] JSON Decode Error: {e}. Response was: {content if 'content' in locals() else 'N/A'}")
            return self._generate_template_resume(resume_text, suggestions_data)
        except Exception as e:
            print(f"[RESUME GEN] Unexpected Error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return self._generate_template_resume(resume_text, suggestions_data)
    
    def _generate_template_resume(self, resume_text, suggestions_data):
        """
        Generate a template resume when AI is unavailable.
        """
        suggestions = suggestions_data.get("suggestions", [])
        
        return {
            "contact": {
                "name": "Your Name",
                "email": "your.email@example.com",
                "phone": "+1 (555) 123-4567",
                "location": "City, State"
            },
            "summary": "Experienced professional with a proven track record of delivering results. Apply the suggestions below to enhance this summary with specific achievements and metrics.",
            "experience": [
                {
                    "title": "Your Most Recent Job Title",
                    "company": "Company Name",
                    "location": "City, State",
                    "dates": "MMM YYYY - Present",
                    "achievements": [
                        "Apply suggestion: " + suggestions[0]["after"] if suggestions else "Add quantified achievement here",
                        "Apply suggestion: " + suggestions[1]["after"] if len(suggestions) > 1 else "Add another achievement with metrics"
                    ]
                }
            ],
            "skills": {
                "Technical": ["Skill 1", "Skill 2", "Skill 3"],
                "Tools": ["Tool 1", "Tool 2", "Tool 3"]
            },
            "education": [
                {
                    "degree": "Your Degree",
                    "institution": "University Name",
                    "year": "YYYY"
                }
            ],
            "certifications": [
                "Relevant Certification (Year)"
            ],
            "_is_demo": True
        }
    
    def create_docx(self, resume_data, output_path):
        """
        Create a Word document (.docx) from resume data.
        
        Args:
            resume_data: Structured resume content
            output_path: Path to save the .docx file
            
        Returns:
            str: Path to created file
        """
        doc = Document()
        
        # Set document margins (1 inch all around)
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.75)
            section.bottom_margin = Inches(0.75)
            section.left_margin = Inches(0.75)
            section.right_margin = Inches(0.75)
        
        # CONTACT INFORMATION
        contact = resume_data.get("contact", {})
        
        # Name (Large, Bold)
        name_para = doc.add_paragraph()
        name_run = name_para.add_run(contact.get("name", "Your Name"))
        name_run.font.size = Pt(18)
        name_run.font.bold = True
        name_run.font.name = 'Calibri'
        name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Contact Details (Centered)
        contact_parts = []
        if contact.get("email"):
            contact_parts.append(contact["email"])
        if contact.get("phone"):
            contact_parts.append(contact["phone"])
        if contact.get("location"):
            contact_parts.append(contact["location"])
        if contact.get("linkedin"):
            contact_parts.append(contact["linkedin"])
        
        contact_para = doc.add_paragraph(" | ".join(contact_parts))
        contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        contact_para.runs[0].font.size = Pt(10)
        contact_para.runs[0].font.name = 'Calibri'
        
        doc.add_paragraph()  # Spacing
        
        # PROFESSIONAL SUMMARY
        if resume_data.get("summary"):
            self._add_section_header(doc, "PROFESSIONAL SUMMARY")
            summary_para = doc.add_paragraph(resume_data["summary"])
            summary_para.runs[0].font.size = Pt(11)
            summary_para.runs[0].font.name = 'Calibri'
            doc.add_paragraph()  # Spacing
        
        # WORK EXPERIENCE
        experience = resume_data.get("experience", [])
        if experience:
            self._add_section_header(doc, "WORK EXPERIENCE")
            
            for exp in experience:
                # Job Title (Bold)
                title_para = doc.add_paragraph()
                title_run = title_para.add_run(exp.get("title", "Job Title"))
                title_run.font.size = Pt(12)
                title_run.font.bold = True
                title_run.font.name = 'Calibri'
                
                # Company, Location, Dates
                details_para = doc.add_paragraph()
                details_text = f"{exp.get('company', 'Company')} | {exp.get('location', 'Location')} | {exp.get('dates', 'Dates')}"
                details_run = details_para.add_run(details_text)
                details_run.font.size = Pt(10)
                details_run.font.italic = True
                details_run.font.name = 'Calibri'
                
                # Achievements (Bullet Points)
                for achievement in exp.get("achievements", []):
                    bullet_para = doc.add_paragraph(achievement, style='List Bullet')
                    bullet_para.runs[0].font.size = Pt(11)
                    bullet_para.runs[0].font.name = 'Calibri'
                
                doc.add_paragraph()  # Spacing between jobs
        
        # SKILLS & EXPERTISE
        skills = resume_data.get("skills", {})
        if skills:
            self._add_section_header(doc, "SKILLS & EXPERTISE")
            
            for category, skill_list in skills.items():
                if skill_list:
                    skills_para = doc.add_paragraph()
                    category_run = skills_para.add_run(f"{category}: ")
                    category_run.font.bold = True
                    category_run.font.size = Pt(11)
                    category_run.font.name = 'Calibri'
                    
                    skills_run = skills_para.add_run(", ".join(skill_list))
                    skills_run.font.size = Pt(11)
                    skills_run.font.name = 'Calibri'
            
            doc.add_paragraph()  # Spacing
        
        # EDUCATION
        education = resume_data.get("education", [])
        if education:
            self._add_section_header(doc, "EDUCATION")
            
            for edu in education:
                edu_para = doc.add_paragraph()
                degree_run = edu_para.add_run(edu.get("degree", "Degree"))
                degree_run.font.bold = True
                degree_run.font.size = Pt(11)
                degree_run.font.name = 'Calibri'
                
                edu_para.add_run(f" | {edu.get('institution', 'Institution')} | {edu.get('year', 'Year')}")
                edu_para.runs[1].font.size = Pt(11)
                edu_para.runs[1].font.name = 'Calibri'
                
                if edu.get("details"):
                    details_para = doc.add_paragraph(edu["details"])
                    details_para.runs[0].font.size = Pt(10)
                    details_para.runs[0].font.italic = True
                    details_para.runs[0].font.name = 'Calibri'
            
            doc.add_paragraph()  # Spacing
        
        # CERTIFICATIONS
        certifications = resume_data.get("certifications", [])
        if certifications:
            self._add_section_header(doc, "CERTIFICATIONS")
            
            for cert in certifications:
                cert_para = doc.add_paragraph(cert, style='List Bullet')
                cert_para.runs[0].font.size = Pt(11)
                cert_para.runs[0].font.name = 'Calibri'
        
        # Save document
        doc.save(output_path)
        return output_path
    
    def _add_section_header(self, doc, text):
        """Add a formatted section header."""
        header_para = doc.add_paragraph()
        header_run = header_para.add_run(text)
        header_run.font.size = Pt(13)
        header_run.font.bold = True
        header_run.font.name = 'Calibri'
        header_run.font.color.rgb = RGBColor(0, 0, 0)
        
        # Add bottom border
        header_para.paragraph_format.space_after = Pt(6)
    
    def create_pdf(self, resume_data, output_path):
        """
        Create a PDF from resume data.
        For now, we'll create the .docx first and note that PDF conversion
        can be done via docx2pdf or weasyprint in production.
        
        Args:
            resume_data: Structured resume content
            output_path: Path to save the .pdf file
            
        Returns:
            str: Path to created file (or docx if PDF conversion unavailable)
        """
        # For now, create a .docx file
        # In production, you can use docx2pdf or weasyprint for conversion
        docx_path = output_path.replace('.pdf', '.docx')
        self.create_docx(resume_data, docx_path)
        
        # TODO: Add PDF conversion here
        # from docx2pdf import convert
        # convert(docx_path, output_path)
        
        return docx_path  # Return docx for now

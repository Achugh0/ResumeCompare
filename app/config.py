import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        # Flask
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
        self.DEBUG = True

        # AI
        self.AI_PROVIDER = "openai"
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

        # Folders
        base_dir = os.getcwd()
        self.UPLOAD_FOLDER = os.path.join(base_dir, "uploads")
        self.DOWNLOADS_FOLDER = os.path.join(base_dir, "downloads")

        # Uploads
        self.ALLOWED_EXTENSIONS = {"pdf", "docx"}

        # Weights
        self.SCORING_WEIGHTS = {
            "skills_match": 20,
            "experience_relevance": 18,
            "education_certifications": 15,
            "keywords_density": 12,
            "career_progression": 10,
            "industry_experience": 8,
            "project_complexity": 8,
            "cultural_fit": 4,
            "achievements_metrics": 3,
            "format_presentation": 2,
        }

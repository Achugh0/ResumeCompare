import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        # Flask
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
        self.DEBUG = True

        # Mongo
        self.MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
        self.MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
        self.MONGO_USERNAME = os.getenv("MONGO_USERNAME", "admin")
        self.MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "resumatch2026")
        self.MONGO_DB = os.getenv("MONGO_DB", "resumatch_db")
        self.MONGO_URI = (
            f"mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}"
            f"@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}?authSource=admin"
        )

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
            "career_progr
ession": 10,
            "industry_experience": 8,
            "project_complexity": 8,
            "cultural_fit": 4,
            "achievements_metrics": 3,
            "format_presentation": 2,
        }

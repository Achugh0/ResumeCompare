import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    DEBUG = True

    # Mongo
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USERNAME = os.getenv("MONGO_USERNAME", "admin")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "resumatch2026")
    MONGO_DB = os.getenv("MONGO_DB", "resumatch_db")
    MONGO_URI = (
        f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}"
        f"@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
    )

    # AI
    AI_PROVIDER = "openai"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Folders
    BASE_DIR = os.getcwd()
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    DOWNLOADS_FOLDER = os.path.join(BASE_DIR, "downloads")

    # Uploads
    ALLOWED_EXTENSIONS = {"pdf", "docx"}

    # Weights
    SCORING_WEIGHTS = {
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

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, config):
        self.config = config
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(
                self.config.MONGO_URI, serverSelectionTimeoutMS=5000
            )
            self.client.admin.command("ping")
            self.db = self.client[self.config.MONGO_DB]
            logger.info("MongoDB connected")
        except ConnectionFailure as e:
            logger.error(f"MongoDB connection failed: {e}")

    def save_analysis(self, data):
        if not self.db:
            return None
        data["created_at"] = datetime.utcnow()
        res = self.db.analyses.insert_one(data)
        return str(res.inserted_id)

class Database:
    def __init__(self, config):
        self.config = config
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(
                self.config.MONGO_URI,
                serverSelectionTimeoutMS=5000
            )
            self.client.admin.command("ping")
            self.db = self.client[self.config.MONGO_DB]
            ...
        except ConnectionFailure as e:
            ...

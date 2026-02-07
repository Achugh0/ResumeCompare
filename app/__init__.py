from .config import Config
from .models.database import Database

db = None

def create_app():
    global db

    import logging, os
    logging.basicConfig(level=logging.INFO)

    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), "templates"),
        static_folder=os.path.join(os.getcwd(), "static"),
    )

    config = Config()              # create an instance
    app.config.from_object(config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["DOWNLOADS_FOLDER"], exist_ok=True)

    db = Database(config)          # pass the Config instance
    db.connect()

    ...
    return app

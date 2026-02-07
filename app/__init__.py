import os
import logging
from flask import Flask
from flask_cors import CORS
from .config import Config
from .models.database import Database
from .generators.template_generator import TemplateGenerator

db = None

def create_app():
    global db

    logging.basicConfig(level=logging.INFO)

    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), "templates"),
        static_folder=os.path.join(os.getcwd(), "static"),
    )
    app.config.from_object(Config)
    CORS(app)

    # Ensure folders exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["DOWNLOADS_FOLDER"], exist_ok=True)

    # Init MongoDB
    db = Database(app.config)
    db.connect()

    # Generate templates once
    TemplateGenerator.generate_all_templates(app.config["DOWNLOADS_FOLDER"])

    # Register blueprints
    from .routes.upload import upload_bp
    from .routes.analysis import analysis_bp
    from .routes.templates_routes import templates_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(templates_bp)

    return app

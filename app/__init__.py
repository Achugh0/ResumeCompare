from flask import Flask
from .config import Config
from .models.database import Database
from .generators.template_generator import TemplateGenerator

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

    config = Config()              # instance
    app.config.from_object(config)

    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(config.DOWNLOADS_FOLDER, exist_ok=True)

    db = Database(config)          # pass instance
    db.connect()

    from .routes.upload import upload_bp
    from .routes.analysis import analysis_bp
    from .routes.templates_routes import templates_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(templates_bp)

    TemplateGenerator.generate_all_templates(config.DOWNLOADS_FOLDER)

    return app

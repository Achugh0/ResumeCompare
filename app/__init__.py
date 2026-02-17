import os
import logging
from flask import Flask
from .config import Config
from .generators.template_generator import TemplateGenerator

def create_app():
    logging.basicConfig(level=logging.INFO)

    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), "templates"),
        static_folder=os.path.join(os.getcwd(), "static"),
    )

    config = Config()  # instance
    app.config.from_object(config)

    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(config.DOWNLOADS_FOLDER, exist_ok=True)

    # Generate Word templates
    TemplateGenerator.generate_all_templates(config.DOWNLOADS_FOLDER)

    # Register blueprints
    from .routes.upload import upload_bp
    from .routes.analysis import analysis_bp
    from .routes.templates_routes import templates_bp
    from .routes.improve_resume import improve_resume_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(templates_bp)
    app.register_blueprint(improve_resume_bp)

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from app import models  # registra todos los modelos en el metadata

    from app.routes import main
    app.register_blueprint(main)

    from app.controllers import register_blueprints
    register_blueprints(app)

    return app

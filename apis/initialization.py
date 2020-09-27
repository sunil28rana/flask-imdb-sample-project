from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from apis.common import app_settings


db = SQLAlchemy()
migrate = Migrate(compare_type=True)


def configure_app():
    app = Flask(__name__)
    app.config.from_object(app_settings)
    db.init_app(app)
    migrate.init_app(app, db)
    return app


def register_blueprint(app):
    from apis.admin.admin_api import blueprint as admin_bp
    from apis.v1.v1_api import blueprint as v1_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(v1_bp)

from flask import Flask
from app.database import db, init_db
from app.controllers.tasks_controller import tasks_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    init_db(app)

    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    return app

# app/main.py
from flask import Flask, render_template
from app.database import db, init_db
from app.controllers.tasks_controller import tasks_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    init_db(app)

    
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    
    @app.route('/')
    def index():
        return "Ve a http://127.0.0.1:5000/ui/tasks para ver la interfaz."

    
    @app.route('/ui/tasks')
    def ui_tasks():
        return render_template('tasks.html')

    return app





if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

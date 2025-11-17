from flask import Flask, redirect, url_for, Blueprint, request, jsonify, render_template
from flask_login import LoginManager, login_required, current_user
from flask_mail import Mail
from datetime import timedelta
from auth import auth_bp
from models import db, User, Task
import os

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['POSTGRES_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    if request.path.startswith('/tasks'):
        return jsonify({'error': 'Unauthorized'}), 401
    return redirect(url_for('auth.login'))

@app.before_request
def session_management():
    app.permanent_session_lifetime = timedelta(hours=8)

main_bp = Blueprint('main', __name__)

@main_bp.route('/index')
@login_required
def index():
    return render_template('index.html', email=current_user.email)

@main_bp.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    tasks_data = [
        {
            'id': t.id,
            'content': t.content,
            'done': t.done,
            'pos_x': t.pos_x,
            'pos_y': t.pos_y,
            'page': t.page,
        } for t in tasks
    ]
    return jsonify(tasks_data)

@main_bp.route('/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.get_json()
    content = data.get('content')
    pos_x = data.get('pos_x', 10)
    pos_y = data.get('pos_y', 10)
    page = data.get('page', 1)
    if not content:
        return jsonify({'error': 'Content required'}), 400
    new_task = Task(
        user_id=current_user.id,
        content=content,
        done=False,
        pos_x=pos_x,
        pos_y=pos_y,
        page=page
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id})

@main_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    data = request.get_json()
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    for field in ['content', 'done', 'pos_x', 'pos_y', 'page']:
        if field in data:
            setattr(task, field, data[field])
    db.session.commit()
    return jsonify({'success': True})

@main_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'success': True})

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)

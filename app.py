from flask import Flask, redirect, url_for, Blueprint, request, jsonify, render_template
from flask_login import LoginManager, login_required, current_user, UserMixin
from flask_mail import Mail
from flask_pymongo import PyMongo
from datetime import timedelta
from auth import auth_bp
from bson.objectid import ObjectId
import os

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# Initialize Flask extensions
mongo = PyMongo(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# User class for flask-login, wrapping MongoDB user doc
class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.email = user_doc['email']

@login_manager.user_loader
def load_user(user_id):
    user_doc = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user_doc:
        return User(user_doc)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    if request.path.startswith('/tasks'):
        return jsonify({'error': 'Unauthorized'}), 401
    return redirect(url_for('auth.login'))

@app.before_request
def session_management():
    app.permanent_session_lifetime = timedelta(hours=8)

# Blueprint for main app routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/index')
@login_required
def index():
    return render_template('index.html', email=current_user.email)

@main_bp.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    user = mongo.db.users.find_one({'_id': ObjectId(current_user.id)})
    tasks_cursor = mongo.db.tasks.find({'user_id': user['_id']})
    tasks_data = []
    for t in tasks_cursor:
        tasks_data.append({
            'id': str(t['_id']),
            'content': t['content'],
            'done': t.get('done', False),
            'pos_x': t.get('pos_x', 10),
            'pos_y': t.get('pos_y', 10),
            'page': t.get('page', 1),
        })
    return jsonify(tasks_data)

@main_bp.route('/tasks', methods=['POST'])
@login_required
def add_task():
    user = mongo.db.users.find_one({'_id': ObjectId(current_user.id)})
    data = request.get_json()
    content = data.get('content')
    pos_x = data.get('pos_x', 10)
    pos_y = data.get('pos_y', 10)
    page = data.get('page', 1)
    if not content:
        return jsonify({'error': 'Content required'}), 400

    task = {
        'user_id': user['_id'],
        'content': content,
        'done': False,
        'pos_x': pos_x,
        'pos_y': pos_y,
        'page': page
    }
    result = mongo.db.tasks.insert_one(task)
    return jsonify({'id': str(result.inserted_id)})

@main_bp.route('/tasks/<task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    user = mongo.db.users.find_one({'_id': ObjectId(current_user.id)})
    data = request.get_json()
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id), 'user_id': user['_id']})
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    update_fields = {}
    for field in ['content', 'done', 'pos_x', 'pos_y', 'page']:
        if field in data:
            update_fields[field] = data[field]

    mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': update_fields})
    return jsonify({'success': True})

@main_bp.route('/tasks/<task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    user = mongo.db.users.find_one({'_id': ObjectId(current_user.id)})
    result = mongo.db.tasks.delete_one({'_id': ObjectId(task_id), 'user_id': user['_id']})
    if result.deleted_count == 0:
        return jsonify({'error': 'Task not found'}), 404
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

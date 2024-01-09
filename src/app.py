from flask import Flask, g, render_template, send_from_directory, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_socketio import SocketIO
from dotenv import load_dotenv
from src.callback import github_callback_blueprint
from src.webhook import github_webhook_blueprint
from src.database import init_database, create_connection, query_user
from src.apis import rest_apis_blueprint
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)
socketio = SocketIO(app)

app.register_blueprint(github_callback_blueprint)
app.register_blueprint(github_webhook_blueprint)
app.register_blueprint(rest_apis_blueprint)

with app.app_context():
    init_database()

@socketio.on('message', namespace='/ws')
def handle_message(message):
    print('[client] ' + message)

@app.route('/')
def index():
    return render_template('index.html',
        client_id=os.environ.get('GITHUB_OAUTH_CLIENT_ID'),
        callback_url=os.environ.get('GITHUB_OAUTH_CALLBACK_URL')
    )

@app.route('/dashboard')
def dashboard():
    github_app_id = os.environ.get('GITHUB_APP_NAME')
    return render_template('dashboard.html',
        github_installation_url=f'https://github.com/apps/{github_app_id}/installations/select_target'
    )

@app.route('/login')
def login():
    """
    Mock implementation of the login route. This function simulates a login process
    by returning a default user's details. Note that no actual user authentication is performed here.
    This is a placeholder for demonstration purposes.

    The returned user data includes the user's ID, username, JWT, and avatar URL.
    Importantly, the `github_access_token` is not exposed to the client for security reasons,
    as it should only be used server-side to interact with the GitHub API.
    """
    conn = create_connection()
    [userid, username, jwt, *_] = query_user(conn, 'shiqimei')
    return jsonify({
        'userid': userid,
        'username': username,
        'jwt': jwt,
        'avatar': '/static/images/avatar.jpeg'
    })

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'images/logo.png')

def dev():
    port = 8080
    socketio.run(app, debug=True, host='0.0.0.0', port=port)

if __name__ == '__main__':
    dev()
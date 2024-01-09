from flask import Flask, g, render_template, send_from_directory, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from src.callback import github_callback_blueprint
from src.database import init_database, create_connection, query_user
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

app.register_blueprint(github_callback_blueprint)

with app.app_context():
    init_database()

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db_connection', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html',
        client_id=os.environ.get('GITHUB_OAUTH_CLIENT_ID'),
        callback_url=os.environ.get('GITHUB_OAUTH_CALLBACK_URL')
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
        'avatar': '/avatar.jpeg'
    })

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('assets', 'logo.png')

@app.route('/avatar.jpeg')
def avatar():
    return send_from_directory('assets', 'avatar.jpeg')

def dev():
    app.run(debug=True, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    dev()
from flask import Flask, g, render_template, send_from_directory
from dotenv import load_dotenv
from src.callback import github_callback_blueprint
from src.database import init_database
import os

app = Flask(__name__)
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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('assets', 'logo.png')

@app.route('/avatar.jpeg')
def avatar():
    return send_from_directory('assets', 'avatar.jpeg')

def dev():
    load_dotenv()
    app.run(debug=True, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    dev()
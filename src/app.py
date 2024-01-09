from flask import Flask, render_template, send_from_directory
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
        client_id=os.environ.get('GITHUB_OAUTH_CLIENT_ID'),
        callback_url=os.environ.get('GITHUB_OAUTH_CALLBACK_URL')
    )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('assets', 'logo.png')

def dev():
    load_dotenv()
    app.run(debug=True, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    dev()
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('assets', 'logo.png')

def dev():
    app.run(debug=True, port=8080)

if __name__ == '__main__':
    dev()
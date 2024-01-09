from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, Flask!"

def dev():
    app.run(debug=True, port=8080)

if __name__ == '__main__':
    dev()
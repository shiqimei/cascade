from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, Flask!"

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
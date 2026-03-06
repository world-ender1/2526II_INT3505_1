from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Server Flask don gian da chay!"

if __name__ == '__main__':
    app.run(port=5000)
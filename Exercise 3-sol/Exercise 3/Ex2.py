from flask import Flask

app = Flask(__name__)

@app.route('/welcome')

def welcome():
    msg1 = "Welcome to Flask Development!"
    msg2 = "This is Labwork 3: Flask/MySQL/API"
    return f"<h1>{msg1}</h1><h2>{msg2}</h2>"

if __name__ == '__main__':
    app.run(debug=True)
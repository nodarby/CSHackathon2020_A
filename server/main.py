from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    message = "This is main page"
    return message

@app.route("/result")
def result():
    message = "This is result page"
    return message


if __name__ == "__main__":
    app.run(debug=True)
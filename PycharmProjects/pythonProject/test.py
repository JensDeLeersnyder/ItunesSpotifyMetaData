from flask import Flask


app = Flask(__name__)


@app.route("/home")
def output():
    return "Hello World!"


if __name__ == "__main__":
    app.run()

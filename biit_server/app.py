from flask import Flask


# This runs on Firebase/Cloud Run!

app = Flask(__name__)


@app.route("/test")
def test_route():
    return "Ok!"


@app.route("/account", methods=["POST", "GET", "PUT", "DELETE"])
def account_route():
    if request.method == "POST":
        return "OK!"
    elif request.method == "GET":
        return "OK!"
    elif request.method == "PUT":
        return "OK!"
    elif request.method == "DELETE":
        return "OK!"

from flask import Flask


# This runs on Firebase/Cloud Run!

app = Flask(__name__)

@app.route("/test")
def test_route():
    return "Ok!"

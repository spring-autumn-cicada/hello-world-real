from flask import Flask
from flask import render_template
from flask import request
import database_manager as dbHandler

app = Flask(__name__)


@app.route("/login.html")
def aboutlogin():
    return render_template("login.html")


@app.route("/messages.html")
def aboutmessages():
    return render_template("messages.html")


@app.route("/profile.html")
def aboutprofile():
    return render_template("profile.html")


@app.route("/index.html", methods=["GET"])
@app.route("/", methods=["POST", "GET"])
def index():
    data = dbHandler.listExtension()
    return render_template("/index.html", content=data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

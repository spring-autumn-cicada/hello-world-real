from flask import Flask, render_template, redirect, url_for, request, flash, session
import database_manager as dbHandler
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session and flash


@app.route("/")
def home():
    return redirect(url_for("aboutlogin"))


@app.route("/login.html", methods=["GET", "POST"])
def aboutlogin():
    if "user" in session:
        return redirect(url_for("aboutprofile"))
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = dbHandler.get_user(username)
        if user and user[2] == password:
            session["user"] = username
            return redirect(url_for("aboutprofile"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)


@app.route("/messages.html")
def aboutmessages():
    if "user" not in session:
        return redirect(url_for("aboutlogin"))
    return render_template("messages.html")


@app.route("/profile.html")
def aboutprofile():
    if "user" not in session:
        return redirect(url_for("aboutlogin"))
    return render_template("profile.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("aboutlogin"))


@app.route("/index.html", methods=["GET"])
def index():
    data = dbHandler.listExtension()
    return render_template("/index.html", content=data)


@app.route("/signup.html", methods=["GET", "POST"])
def signup():
    if "user" in session:
        return redirect(url_for("aboutprofile"))
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        account_creation_date = datetime.now().strftime("%d/%m/%Y")  # dd/mm/yyyy format
        if dbHandler.get_user(username):
            error = "Username already exists"
        else:
            success = dbHandler.add_user(
                username, password, email, account_creation_date
            )
            if success:
                session["user"] = username
                return redirect(url_for("aboutprofile"))
            else:
                error = "Signup failed"
    return render_template("signup.html", error=error)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

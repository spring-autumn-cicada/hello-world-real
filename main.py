import os
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    session,
)
import database_manager as dbHandler
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key"
# Needed for session and flash

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/update_avatar", methods=["POST"])
def update_avatar():
    if "user" not in session:
        return redirect(url_for("aboutlogin"))
    file = request.files.get("avatar")
    if file and allowed_file(file.filename):
        filename = secure_filename(session["user"] + "_" + file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        # Save the avatar path to the user's profile in your database
        dbHandler.update_avatar(session["user"], filepath)
    return redirect(url_for("aboutprofile"))


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


@app.route("/update_bio", methods=["POST"])
def update_bio():
    if "user" not in session:
        return redirect(url_for("aboutlogin"))
    bio = request.form.get("bio", "")
    dbHandler.update_bio(session["user"], bio)
    return redirect(url_for("aboutprofile"))


@app.route("/messages.html", methods=["GET", "POST"])
def aboutmessages():
    if "user" not in session:
        return redirect(url_for("aboutlogin"))
    current_user = session["user"]

    # Handle search
    search_query = request.args.get("search", "")
    if search_query:
        users = [
            u
            for u in dbHandler.get_all_users(
                exclude_username=current_user, search_query=search_query
            )
        ]
    else:
        # Get recent chats (by last interaction)
        recent_chats = dbHandler.get_recent_chats(current_user)

        # Get all users except self
        all_users = dbHandler.get_all_users(exclude_username=current_user)

        # Users never messaged = all_users - recent_chats
        other_users = [u for u in all_users if u not in recent_chats]
        users = other_users

    # Handle selecting a chat
    selected_user = request.args.get("user")
    messages = []
    if selected_user:
        raw_messages = dbHandler.get_messages(current_user, selected_user)
        messages = []
        for sender, recipient, content, timestamp in raw_messages:
            avatar_url = dbHandler.get_avatar(sender)
            messages.append(
                {
                    "sender": sender,
                    "recipient": recipient,
                    "content": content,
                    "timestamp": timestamp,
                    "avatar_url": avatar_url,
                }
            )

    # Handle sending a message
    if request.method == "POST" and selected_user:
        content = request.form.get("message")
        if content:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dbHandler.add_message(
                current_user,
                selected_user,
                content,
                timestamp,
            )
            return redirect(url_for("aboutmessages", user=selected_user))

    return render_template(
        "messages.html",
        users_recent=recent_chats,
        users_other=other_users,
        selected_user=selected_user,
        messages=messages,
        search_query=search_query,
    )


@app.route("/profile.html")
def aboutprofile():
    if "user" not in session:
        return redirect(url_for("aboutlogin"))
    user = dbHandler.get_user(session["user"])
    username = user[1] if user else ""
    email = user[3] if user else ""
    bio = user[5] if user and len(user) > 5 and user[5] else "No Bio"
    avatar_url = user[6] if user and len(user) > 6 and user[6] else None
    account_creation_date = user[4] if user and len(user) > 4 else ""
    return render_template(
        "profile.html",
        username=username,
        email=email,
        bio=bio,
        avatar_url=avatar_url,
        account_creation_date=account_creation_date,
    )


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
        account_creation_date = datetime.now().strftime("%d/%m/%Y")
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

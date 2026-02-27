from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "mysecretkey123"   # Required for session

# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["user"] = username   # SET session
        return redirect(url_for("home"))
    return render_template("login.html")


# Home Page
@app.route("/home")
def home():
    if "user" in session:            # GET session
        return render_template("home.html", name=session["user"])
    return redirect(url_for("login"))


# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)        # DELETE session
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "yoursecretkey123"  # Needed for session handling

# Dummy credentials (for testing)
USERNAME = "admin"
PASSWORD = "1234"

@app.route('/')
def home():
    # Check if user is logged in
    if "user" in session:
        return render_template("index.html", user=session["user"])
    else:
        return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ---------- STATE ROUTES ----------
@app.route('/karnataka')
def karnataka():
    return render_template("karnataka.html")

@app.route('/kerala')
def kerala():
    return render_template("kerala.html")

@app.route('/tamilnadu')
def tamilnadu():
    return render_template("tamilnadu.html")

@app.route('/maharashtra')
def maharashtra():
    return render_template("maharashtra.html")

@app.route('/gujarat')
def gujarat():
    return render_template("gujarat.html")
# ----------------------------------

if __name__ == "__main__":
    app.run(debug=True)

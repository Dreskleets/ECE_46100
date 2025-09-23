import secrets, sqlite3, os
from flask import Flask, flash, redirect, url_for, render_template, request, session

from datetime import timedelta

app = Flask(__name__)
#Change key for deployment
app.secret_key = secrets.token_hex(16)
#Stores data for 1 minute
app.permanent_session_lifetime = timedelta(minutes = 1)

@app.route("/")
def base():
    return redirect(url_for("home"))

#Home page setup
@app.route("/home")
def home():
    #Simple html script for home page
    return render_template("index.html")

# Temporary test user for login validation
TEST_USER = {
    "email": "test@gmail.com",
    "password": "pass"
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == TEST_USER["email"] and password == TEST_USER["password"]:
            session.permanent = True  # Make the session last for app.permanent_session_lifetime
            session["user"] = email
            flash("Login successful!", "success")
            return redirect(url_for("user"))  # send to profile page
        else:
            flash("Invalid credentials, try again.", "danger")

        print(f"Login attempt: {email} - {password}")

        return redirect(url_for("user"))  # Redirect to profile page after login

    return render_template("login.html")


@app.route("/user")
def user():
    
    if "user" in session:
        user = session ["user"]
        user_data = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "location": "West Lafayette, IN",
        "bio": "ECE Student exploring software engineering."
    }
        return render_template("user.html", user = user_data)    
    else:
        return redirect(url_for("login"))
    

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/browse")
def browse():
    q = request.args.get("q", "")
    category = request.args.get("category", "")
    sort = request.args.get("sort", "name")

    conn = sqlite3.connect("dummy_data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # --- Get Top 5 Models (by avg_rating)
    cur.execute("""
        SELECT m.id, m.name, m.description, m.category,
               COALESCE(AVG(r.rating), 0) as avg_rating
        FROM models m
        LEFT JOIN reviews r ON m.id = r.model_id
        GROUP BY m.id
        ORDER BY avg_rating DESC
        LIMIT 5
    """)
    top_models = cur.fetchall()

    # --- Build query for browsing
    query = """
        SELECT m.id, m.name, m.description, m.category,
               COALESCE(AVG(r.rating), 0) as avg_rating
        FROM models m
        LEFT JOIN reviews r ON m.id = r.model_id
    """
    conditions = []
    params = []

    if q:
        conditions.append("(m.name LIKE ? OR m.description LIKE ?)")
        params.extend([f"%{q}%", f"%{q}%"])

    if category:
        conditions.append("m.category = ?")
        params.append(category)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY m.id"

    if sort == "rating":
        query += " ORDER BY avg_rating DESC"
    else:
        query += " ORDER BY m.name ASC"

    cur.execute(query, params)
    models = cur.fetchall()
    conn.close()

    return render_template("browse.html", top_models=top_models, models=models)


@app.route("/modelreviews")
def modelreviews():
    
    return render_template("modelReviews.html")

@app.route("/review", methods = ["GET", "POST"])
def review():
    if request.method == "POST":
        ramp = int(request.form["ramp"])
        bus = int(request.form["bus"])
        license = int(request.form["license"])
        size = int(request.form["size"])
        data = int(request.form["data"])
        code = int(request.form["code"])
        
        net_score = (ramp + bus + license + size + data + code) / 6
        
        conn = sqlite3.connect('review_data.db')
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO NetScore (net_score, ramp_up_time_metric, bus_factor_metric, license_metric, size_score_metric, data_score_metric, code_quality_metric)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (net_score, ramp, bus, license, size, data, code))
        conn.commit()
        conn.close() 
        return render_template("thank.html", net_score = net_score)
    
    return render_template("review.html")

if __name__ == "__main__":
    #Allows us to not rerun the server every change
    #Disable for deployment
    app.run(debug=True)
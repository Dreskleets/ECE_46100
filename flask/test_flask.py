from flask import Flask, redirect, url_for, render_template, request, session

from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
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

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user", usr = user))    
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user")
def user():
    
    if "user" in session:
        user = session ["user"]
        return render_template("user.html", user = user)    
    else:
        return redirect(url_for("login"))
    

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("/login"))

if __name__ == "__main__":
    #Allows us to not rerun the server every change
    app.run(debug=True)
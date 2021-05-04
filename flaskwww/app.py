from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/<name>")
def who(name):
    return render_template("login.html", content=name)
    # return "Who are you?"

@app.route("/hi/<username>")
def greet(username):
    return f"Hi there, {username}!"

# @app.route("/admin")
# def admin():
    # return redirect(url_for("home"))

# if __name__ == "__main__":
    # app.run()

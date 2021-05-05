from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

import url_generator

# Bootstrap websites: https://getbootstrap.com/docs/5.0/examples/

app = Flask(__name__)
app.secret_key = 'super secret key'
app.permanent_session_lifetime = timedelta(days=5)
app.config['UPLOAD_FOLDER'] = "./"
app.config['MAX_CONTENT_PATH'] = "10000"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # session.permanent = True  # Make session permanent
        user = request.form["inputname"]
        session["user"] = user
        flash("Login successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in.")
            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out", "info")
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_input_file():
    if request.method == 'POST':
        f = request.files['file']
        target_web = request.form['target_web']
        flash(target_web + " is selected")

        # f.save(secure_filename(f.filename))
        f.save(f.filename)
        flash('Deck has been uploaded successfully')

        # process deck and print urls by given options from form (options like target web etc.)
        deckfile = open("./" + f.filename, "r")
        cards = deckfile.read().split('\n')
        # TODO process and modify card urls based on options from form
        # ...
        deckfile.close()
        return render_template('uploader.html', filename=f.filename, deck=cards)


if __name__ == '__main__':
    app.run(debug = True)


# @app.route("/admin")
# def admin():
    # return redirect(url_for("home"))

if __name__ == "__main__":
    # TODO In production edit these:
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)


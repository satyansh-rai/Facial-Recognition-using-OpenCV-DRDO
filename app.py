from functools import wraps
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Response
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from utils.webcamvideostream import WebcamVideoStream
from utils.face_recog_videostream import FaceRecognitionVideoStream
import cv2
import time
from utils.camera import camera_feed

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "password123"
app.config['MYSQL_DB'] = "firstapp"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# Initializing MySQL

mysql = MySQL(app)

Articles = Articles()

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route("/")
def index():
    """Video streaming home page."""
    return render_template('home.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    video_stream = WebcamVideoStream()
    return Response(camera_feed(video_stream.start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/face_recog')
def face_recog():
    """Video streaming route. Put this in the src attribute of an img tag."""
    video_stream = FaceRecognitionVideoStream()
    return Response(camera_feed(video_stream.start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/articles")
def articles():
    return render_template('articles.html', articles=Articles)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))


        # Create cursor
        cur = mysql.connection.cursor()

        with cur:
            cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

            # Commit to database
            mysql.connection.commit()
        flash("You are now registered", "success")
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

# User login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form fields
        username = request.form["username"]
        password_candidate = request.form["password"]

        # Create cursor
        cur = mysql.connection.cursor()

        with cur:
            result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

            if result > 0:
                # Get stored hash
                data = cur.fetchone()
                password = data["password"]

                # Compare the passwords
                if sha256_crypt.verify(password_candidate, password):
                    # Passed
                    session['logged_in'] = True
                    session['username'] = username

                    flash('You are now logged in!', "success")
                    return redirect(url_for('dashboard'))
                    # app.logger.info("Password Matched :)")
                
                else:
                    # app.logger.info("Password Mismatch :(")
                    error = "Invalid Login"
                    return render_template("login.html", error=error)
                
            else:
                # app.logger.info("No User!")
                error = "Username not found"
                return render_template("login.html", error=error)
        
    
    return render_template("login.html")

# Check if user is logged in

def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash('Please login to access this.', "danger")
            return redirect(url_for('login'))
        
    return decorated_function

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Your are logged out!", "success")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    return  render_template("dashboard.html")

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    details = [
        {'body': 'name', 'author': user},
        {'body': 'email id', 'author': user}
    ]
    return render_template('user.html', user=user, posts=posts)

if __name__ == '__main__':
    app.secret_key="secret123"
    app.run(debug=True, threaded=True)

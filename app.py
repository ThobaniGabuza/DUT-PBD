from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import os
from flask import Flask, session
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/departments")
def departments():
    return render_template("departments.html")

@app.route("/about")
def about():
    return render_template("about.html")

#Route for the sign in button to take you me to the login.html page
@app.route('/signin')
def signin():
    return render_template('login.html')

#Route for reporting incidents
@app.route('/report')
def report():

    return render_template('report.html')

#login routes and validity check if the student enters wronng details
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST' and 'login' in request.form:
        username = request.form['username']
        password = request.form['password']
        if not username.endswith('@dut4life.ac.za'):
            error = 'Invalid username. Please enter a valid DUT email address.'
        elif len(password) < 6 or len(password) > 8:
            error = 'Invalid password. Please enter a password between 6 to 8 characters.'
        else:
            # If both the username and password are valid, redirect to the report.html page
            return redirect(url_for('report'))
    return render_template('login.html', error=error)

#form routes
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campus = db.Column(db.String(50), nullable=False)
    faculty = db.Column(db.String(50), nullable=False)
    building = db.Column(db.String(50), nullable=False)
    block = db.Column(db.String(50), nullable=False)
    maintenance_issue = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(10), nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)

# Route to handle form submission
@app.route('/reportsubmitted', methods=['POST'])
def reportsubmitted():
    campus = request.form['campus']
    faculty = request.form['faculty']
    building = request.form['building']
    block = request.form['block']
    maintenance_issue = request.form['maintenance-issue']
    severity = request.form['severity']
    image = request.files.get('image')

    # Check if image file was uploaded and is of valid format
    if image and allowed_file(image.filename):
        # Save the file to the uploads folder
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Create a new table in the database with the user's report information
        report = Report(campus=campus, faculty=faculty, building=building, block=block, maintenance_issue=maintenance_issue, severity=severity, image_filename=filename)
        db.session.add(report)
        db.session.commit()
        # Return success message
        return redirect(url_for('admin'))
    else:
        # Return error message
        return render_template('reportsub.html')


# Function to check if uploaded file is of a valid image format
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


#admin login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST' and 'login' in request.form:
        username = request.form['username']
        password = request.form['password']
        if not username.endswith('@dut4life.ac.za'):
            error = 'Invalid username. Please enter a valid DUT email address.'
        elif len(password) < 6 or len(password) > 8:
            error = 'Invalid password. Please enter a password between 6 to 8 characters.'
        else:
            # If both the username and password are valid, redirect to the report.html page
            return redirect(url_for('admin'))
    return render_template('admin.html', error=error)

@app.route('/admin')
def admin():
    reports = Report.query.all()
    return render_template('admin.html', reports=reports)





from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)


# -------------------------
# DATABASE MODELS
# -------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))


class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    reason = db.Column(db.String(200))
    status = db.Column(db.String(50))


class Timesheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.String(50))
    hours = db.Column(db.String(50))


# -------------------------
# ROUTES
# -------------------------

@app.route('/')
def home():
    return render_template("login.html")


# -------------------------
# LOGIN
# -------------------------

@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:

        session['user_id'] = user.id
        session['role'] = user.role

        if user.role == "admin":
            return redirect('/admin')

        elif user.role == "employee":
            return redirect('/user')

    return "Invalid Login"


# -------------------------
# LOGOUT
# -------------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# -------------------------
# ADMIN DASHBOARD
# -------------------------

@app.route('/admin')
def admin_dashboard():

    if session.get('role') != "admin":
        return "Unauthorized"

    users = User.query.all()
    leaves = Leave.query.all()

    return render_template("admin_dashboard.html", users=users, leaves=leaves)


# -------------------------
# USER DASHBOARD
# -------------------------

@app.route('/user')
def user_dashboard():

    if session.get('role') != "employee":
        return "Unauthorized"

    return render_template("user_dashboard.html")


# -------------------------
# APPLY LEAVE
# -------------------------

@app.route('/apply_leave', methods=['GET', 'POST'])
def apply_leave():

    if session.get('user_id') is None:
        return redirect('/')

    if request.method == "POST":

        reason = request.form['reason']

        leave = Leave(
            user_id=session['user_id'],
            reason=reason,
            status="Pending"
        )

        db.session.add(leave)
        db.session.commit()

        return redirect('/user')

    return render_template("apply_leave.html")


# -------------------------
# TIMESHEET
# -------------------------

@app.route('/timesheet', methods=['GET', 'POST'])
def timesheet():

    if session.get('user_id') is None:
        return redirect('/')

    if request.method == "POST":

        date = request.form['date']
        hours = request.form['hours']

        t = Timesheet(
            user_id=session['user_id'],
            date=date,
            hours=hours
        )

        db.session.add(t)
        db.session.commit()

        return redirect('/user')

    return render_template("timesheet.html")


# -------------------------
# APPROVE LEAVE
# -------------------------

@app.route('/approve/<int:id>')
def approve_leave(id):

    if session.get('role') != "admin":
        return "Unauthorized"

    leave = Leave.query.get(id)

    leave.status = "Approved"

    db.session.commit()

    return redirect('/admin')


# -------------------------
# RUN APP
# -------------------------

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        # Create default admin
        if not User.query.filter_by(username="admin").first():

            admin = User(
                username="admin",
                password="admin123",
                role="admin"
            )

            db.session.add(admin)
            db.session.commit()

        # Create default employee
        if not User.query.filter_by(username="employee").first():

            emp = User(
                username="employee",
                password="123",
                role="employee"
            )

            db.session.add(emp)
            db.session.commit()

    app.run(debug=True)
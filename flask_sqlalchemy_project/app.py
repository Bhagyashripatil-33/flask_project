from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret123'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username=username,password=password)
        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username,password=password).first()

        if user:
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "Invalid Username or Password"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    users = User.query.all()
    return render_template('dashboard.html',users=users)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        new_user = User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/dashboard')

    return render_template('add_user.html')

@app.route('/delete/<int:id>')
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        db.session.commit()
        return redirect('/dashboard')
    return render_template('edit_user.html',user=user)

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
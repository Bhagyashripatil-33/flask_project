from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secretkey"

# Temporary storage (list)
students = []

# ------------------ LOGIN PAGE ------------------
@app.route('/')
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "1234":
        session['admin'] = "Bhagyashri"
        return redirect(url_for('register'))
    else:
        return "Invalid Login <a href='/'>Try Again</a>"

# ------------------ REGISTER PAGE ------------------
@app.route('/register')
def register():
    if 'admin' in session:
        return render_template("register.html")
    else:
        return redirect(url_for('login_page'))

# ------------------ CONFIRM DETAILS ------------------
@app.route('/confirm', methods=['POST'])
def confirm():
    name = request.form['name']
    age = request.form['age']
    course = request.form['course']

    return render_template("confirm.html", name=name, age=age, course=course)

# ------------------ SAVE DATA ------------------
@app.route('/save', methods=['POST'])
def save():
    name = request.form['name']
    age = request.form['age']
    course = request.form['course']

    students.append({
        "name": name,
        "age": age,
        "course": course
    })

    return redirect(url_for('showdata'))

# ------------------ SHOW DATA ------------------
@app.route('/showdata')
def showdata():
    return render_template("showdata.html", students=students)

# ------------------ LOGOUT ------------------
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
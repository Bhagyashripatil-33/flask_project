
from flask import Flask, render_template, request, redirect, session
import sqlite3, datetime

app = Flask(__name__)
app.secret_key = "supersecret"
DB = "hrm.db"

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    con = db()

    con.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )''')

    con.execute('''CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        department TEXT,
        salary INTEGER
    )''')

    con.execute('''CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER,
        date TEXT,
        status TEXT
    )''')

    con.execute('''CREATE TABLE IF NOT EXISTS leave_requests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER,
        days INTEGER,
        reason TEXT,
        status TEXT
    )''')

    con.execute("INSERT OR IGNORE INTO users(id,username,password,role) VALUES (1,'admin','admin','admin')")

    con.commit()
    con.close()

def login_required():
    return "user" in session

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]

        con=db()
        user=con.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p)).fetchone()
        con.close()

        if user:
            session["user"]=u
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect("/")

    con=db()
    emp=con.execute("SELECT COUNT(*) c FROM employees").fetchone()["c"]
    leave=con.execute("SELECT COUNT(*) c FROM leave_requests").fetchone()["c"]
    con.close()

    return render_template("dashboard.html",emp=emp,leave=leave)

@app.route("/employees")
def employees():
    if not login_required():
        return redirect("/")

    con=db()
    emps=con.execute("SELECT * FROM employees").fetchall()
    con.close()

    return render_template("employees.html",emps=emps)

@app.route("/add_employee", methods=["GET","POST"])
def add_employee():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        dept=request.form["department"]
        salary=request.form["salary"]

        con=db()
        con.execute("INSERT INTO employees(name,email,department,salary) VALUES(?,?,?,?)",(name,email,dept,salary))
        con.commit()
        con.close()

        return redirect("/employees")

    return render_template("add_employee.html")

@app.route("/attendance/<int:id>")
def attendance(id):
    today=str(datetime.date.today())

    con=db()
    con.execute("INSERT INTO attendance(emp_id,date,status) VALUES(?,?,?)",(id,today,"Present"))
    con.commit()
    con.close()

    return redirect("/employees")

@app.route("/leave/<int:id>", methods=["GET","POST"])
def leave(id):
    if request.method=="POST":
        days=request.form["days"]
        reason=request.form["reason"]

        con=db()
        con.execute("INSERT INTO leave_requests(emp_id,days,reason,status) VALUES(?,?,?,?)",(id,days,reason,"Pending"))
        con.commit()
        con.close()

        return redirect("/employees")

    return render_template("leave.html",id=id)

@app.route("/leaves")
def leaves():
    con=db()
    leaves=con.execute("""
    SELECT leave_requests.*, employees.name 
    FROM leave_requests 
    JOIN employees ON employees.id=leave_requests.emp_id
    """).fetchall()
    con.close()

    return render_template("leave_list.html",leaves=leaves)

@app.route("/approve/<int:id>")
def approve(id):
    con=db()
    con.execute("UPDATE leave_requests SET status='Approved' WHERE id=?",(id,))
    con.commit()
    con.close()
    return redirect("/leaves")

@app.route("/salary/<int:id>")
def salary(id):
    con=db()

    emp=con.execute("SELECT * FROM employees WHERE id=?",(id,)).fetchone()
    attendance=con.execute("SELECT COUNT(*) c FROM attendance WHERE emp_id=?",(id,)).fetchone()["c"]

    salary=(emp["salary"]/30)*attendance

    con.close()

    return render_template("salary.html",emp=emp,attendance=attendance,salary=salary)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

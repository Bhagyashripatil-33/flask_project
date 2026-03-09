from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    con = sqlite3.connect('Employees.db')
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Employee(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        sal INTEGER NOT NULL
    )
    """)

    con.commit()
    con.close()

create_table()
app = Flask(__name__)

# Show employees
@app.route('/')
def index():

    con = sqlite3.connect("Employees.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM Employee")
    data = cur.fetchall()

    con.close()

    return render_template("index.html", employees=data)


# Add employee
@app.route('/add', methods=["GET","POST"])
def add():

    if request.method == "POST":

        id = request.form['id']
        name = request.form['name']
        sal = request.form['sal']

        con = sqlite3.connect("Employees.db")
        cur = con.cursor()

        cur.execute("INSERT INTO Employee VALUES(?,?,?)",(id,name,sal))

        con.commit()
        con.close()

        return redirect('/')

    return render_template("add.html")


# Delete employee
@app.route('/delete/<int:id>')
def delete(id):

    con = sqlite3.connect("Employees.db")
    cur = con.cursor()

    cur.execute("DELETE FROM Employee WHERE id=?",(id,))

    con.commit()
    con.close()

    return redirect('/')


# Update employee
@app.route('/edit/<int:id>', methods=["GET","POST"])
def edit(id):

    con = sqlite3.connect("Employees.db")
    cur = con.cursor()

    if request.method == "POST":

        name = request.form['name']
        sal = request.form['sal']

        cur.execute("UPDATE Employee SET name=?, sal=? WHERE id=?",(name,sal,id))

        con.commit()
        con.close()

        return redirect('/')

    cur.execute("SELECT * FROM Employee WHERE id=?",(id,))
    emp = cur.fetchone()

    con.close()

    return render_template("edit.html", emp=emp)


if __name__ == "__main__":
    app.run(debug=True)
    
    

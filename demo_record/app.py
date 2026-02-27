from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    students = [
        {"id": 1, "name": "Bhagyashri", "course": "MCA"},
        {"id": 2, "name": "Rahul", "course": "BCA"},
        {"id": 3, "name": "Sneha", "course": "BSc IT"}
    ]
    return render_template("home.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)
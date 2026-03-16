from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

@app.route("/")
def home():
    return render_template("dashboard.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)